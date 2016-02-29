Client's Tests
================

Each test checks the clients behavior on different situation of the game functions.

Lobby related
---------------------

| Create_Game Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct create                                                          | ✔             | ✔             |
| The gamename is too long                                          | ✔             | ✔             |
| The Game already exists                                          | ✔             | ✔             |


| Join_Game Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct join                                                          | ✔             | ✔             |
| The room is full                                          | ✔             | ✔             |
| The Game doesn't exist                                          | ✔             | ✔             |

Game related
---------------------

| Ship_Placement Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct ship_placement                                                          | ✔             | ✔             |
| The ship_placement has collision with border                                          | ✔             | ✔             |
| The ship_palcement has collision with other ships                                          | ✔             | ✔             |
| The ship_palcement is diagonal                                          | ✔             | ✔             |
| The ship is too long                                          | ✔             | ✔             |
| The ship is too short                                          | ✔             | ✔             |
| Too Many Carriers are added                                          | ✔             | ✔             |
| Too Many Battleships are added                                          | ✔             | ✔             |
| Too Many Cruisers are added                                          | ✔             | ✔             |
| Too Many Destroyers are added                                          | ✔             | ✔             |

| Move Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct move                                                          | ✔             | ✔             |
| The move has illegal ship_index                                          | ✔             | ✔             |
| The move exceeds the game_boundry                                          | ✔             | ✔             |

| Attack Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct attack                                                          | ✔             | ✔             |
| The attack is out of game_boundry                                          | ✔             | ✔             |

| Special_Attack Test                                                                  |  Correct Response   |
|-----------------------------------------------------------------------|--------------|
| Correct special_attack                                                          | ✔             | ✔             |
| The specail-attack is out of game_boundry                                           | ✔             | ✔             |
| The special_attacks are used more than 3 times                                          | ✔             | ✔             |


