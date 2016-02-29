Testing Protocol
================

Server Tests
------------

Each test uses the server of one team and a client of both teams.

###  Basic game management

| Test                                                                  |  PE2 Server   |  PE4 Server   |
|-----------------------------------------------------------------------|---------------|---------------|
|Get connected                                                          | ✔             | ✔             |
|Server found by UDP-Discovery                                          | ✔             | ✔             |
|Multiple games shown in lobby                                          | ✔             | ✔             |
|Game create successful                                                 | ✔             | ✔             |
|Game join successful                                                   | ✔             | ✔             |
|Server deletes created game when client leaves                         | ✔             | ✔             |
|Wait for opponent                                                      | ✔             | ✔             |
|Place ships successful                                                 | ✔             | ✔             |
|Wait for own turn                                                      | ✔             | ✔             |
|Run multiple games at the same server at the same time                 | ✔             | ✔             |

###  Different attacks and movements

| Test                                                                  |  PE2 Server   |  PE4 Server   |
|-----------------------------------------------------------------------|---------------|---------------|
|Attack water -> unfog field                                            | ✔             | ✔             |
|Attack part of ship -> unfog field                                     | ✔             | ✔             |
|Re-attack part of ship -> nothing special happens                      | ✔             | ✔             |
|Special attack in the middle of the field                              | ✔             | ✔             |
|Special attack in bottom-left corner (0,0)                             | ✔             | ✔             |
|Special attack in top-left corner (0,15) -> should fail                | ✔             | ✔             |
|Special attack in the bottom-right corner (15,0) -> should fail        | ✔             | ✔             |
|Special attack in the top-right corner (15,15) -> should fail          | ✔             | ✔             |
|More than three special attacks                                        | ✔             | ✔             |
|Simple move ship                                                       | ✔             | ✔             |
|Move ship onto other ship -> should fail                               | ✔             | ✔             |
|Move ship against playing field border -> should fail                  | ✔             | ✔             |
|Move ship out of the fog                                               | ✔             | ✔             |
|Move ship back into the fog                                            | ✔             | ✔             |
|Move completely damaged ship -> should fail                            | ✔             | ✔             |
|Move onto completely damaged (sunken) -> should fail                   | ✔             | ✔             |

###  Different game endings

| Test                                                                  |  PE2 Server   |  PE4 Server   |
|-----------------------------------------------------------------------|---------------|---------------|
|Game ends: one wins and one loses                                      | ✔             | ✔             |
|Leave game                                                             | ✔             | ✔             |
|Capitulate                                                             | ✔             | ✔             |

###  Optional: UDP Discovery

| Test                                                                  |  PE2 Server   |  PE4 Server   |
|-----------------------------------------------------------------------|---------------|---------------|
|Server found by UDP-Discovery                                          | ✔             | ✔             |

###  Optional: Chat

| Test                                                                  |  PE2 Server   |  PE4 Server   |
|-----------------------------------------------------------------------|---------------|---------------|
|Client sends message                                                   | ✔             | ✔             |
|All clients receive the message                                        | ✔             | ✔             |