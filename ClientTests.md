Client's Tests
================

Each test checks the clients behavior on different situation of the game functions.

Lobby related
---------------------

| Create_Game Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct create                                                          | ✔             | ✔             |
|Case 2: The gamename is too long                                          | ✔             | ✔             |
|Case 3: The Game already exists                                          | ✔             | ✔             |


| Join_Game Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct join                                                          | ✔             | ✔             |
|Case 2: The room is full                                          | ✔             | ✔             |
|Case 3: The Game doesn't exist                                          | ✔             | ✔             |

Game related
---------------------

| Ship_Placement Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct ship_placement                                                          | ✔             | ✔             |
|Case 2: The ship_placement has collision with border                                          | ✔             | ✔             |
|Case 3: The ship_palcement has collision with other ships                                          | ✔             | ✔             |
|Case 4: The ship_palcement is diagonal                                          | ✔             | ✔             |
|Case 5: The ship is too long                                          | ✔             | ✔             |
|Case 6: The ship is too short                                          | ✔             | ✔             |
|Case 7: Too Many Carriers are added                                          | ✔             | ✔             |
|Case 8: Too Many Battleships are added                                          | ✔             | ✔             |
|Case 9: Too Many Cruisers are added                                          | ✔             | ✔             |
|Case 10: Too Many Destroyers are added                                          | ✔             | ✔             |

| Move Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct move                                                          | ✔             | ✔             |
|Case 2: The move has illegal ship_index                                          | ✔             | ✔             |
|Case 3: The move exceeds the game_boundry                                          | ✔             | ✔             |

| Attack Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct attack                                                          | ✔             | ✔             |
|Case 2: The attack is out of game_boundry                                          | ✔             | ✔             |

| Special_Attack Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
|Case 1: Correct special_attack                                                          | ✔             | ✔             |
|Case 2: The specail-attack is out of game_boundry                                           | ✔             | ✔             |
|Case 3: The special_attacks are used more than 3 times                                          | ✔             | ✔             |


