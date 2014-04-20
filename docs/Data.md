Data Design:
----

1.	配置信息：永久有效

    存放在key：MoePadConf中。包括微博的App Key/Secret，MoePad程序所在域名，同一条目两次发送之间的间隔。

2.  Token信息：带过期时间，用登陆时返回的expires_in计算

    存放在key：WeiboAuth(original/retweet)中，分别保存发送原创微博，转推微博的OAuth授权信息。保存了access token, expires_in, user_type, uid。目前应该只使用了original。

3.  待发送条目池：带过期时间，一个条目如果长期轮不上发送就删除，定为24小时。

    分为三类，Verifying, Verified和Edited，分别是新创建的条目（待审核），通过审核的新条目以及编辑改动的 老条目，优先发送通过审核的新条目，只有当没有新条目时，才发送编辑导致更新的条目。同时，如果一个新创建的条目，1小时内没有审核的动作，就视为通过审核，移入Verified池中。

    Verified和Edited使用字符串存放，Verifying由于要计算过期时间（过期之后还要用到其信息，不能使用redis自己的过期机制，除非能hook过期事件）使用Ordered Set存放，score是其过期时间。

    对于新条目，每次update的时候都检查一下是否已经删除，发送之前也检查是否删除，是则从队列中移除。判断标准是，api返回的query里的pages里是否存在－1这个key。同时－1这个key对应的value里面含有missing这个key。请求`http://zh.moegirl.org/api.php?format=json&action=query&prop=info&titles=%E7%99%BE%E5%90%88(%E9%87%8D%E5%AE%9A%E5%90%91)`页面返回。

    ```
    {
    query: {
        pages: {
            -1: {
                ns: 0,
                title: "义乌哪里有小姐",
                missing: ""
                }
            }
        }
    }

    ```

    对于每个待考察条目，增加一个validation，检查是否是重定向页面。请求`http://zh.moegirl.org/api.php?format=json&action=query&prop=info&redirects&titles=%E7%99%BE%E5%90%88(%E6%B6%88%E6%AD%A7%E4%B9%89)`页面返回。即检查query里是否有redirects这个key。有则忽略，不插入任务队列。

    ```
    {
    query: {
        redirects: [
        {
            from: "百合(消歧义)",
            to: "百合(消歧义页)"
            }
            ],
            pages: {
                6116: {
                    pageid: 6116,
                    ns: 0,
                    title: "百合(消歧义页)",
                    contentmodel: "wikitext",
                    pagelanguage: "zh",
                    touched: "2013-07-31T06:48:22Z",
                    lastrevid: 98483,
                    counter: "",
                    length: 1085
                }
            }
        }
    }
    ```


5.  已发送条目池：带过期时间，根据MoePadConf里设置的发送间隔确定

6.  从mediawiki api获取的字符串均为unicode

7.  各队列都约定左进右出