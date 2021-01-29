# ROLEPY

Tools to work with focused proofs in sequent calculi.

## Changelog

- 28 January 2021: Lots of refactoring and reorganization.

## Sample output

```
Context 1                                   Context 2
------------------------------------------  ------------------------------------------
A1                                          A1
And(A1, A2)                                 And(A1, A2)
Not(A2)                                     Not(A2)
Impl(A12, Not(A2))                          Impl(A12, Not(A2))
A4                                          A4
Or(Impl(X2, A10), Not(A3))                  Or(Impl(X2, A10), Not(A3))
A5                                          A5
Or(A7, Not(Not(And(A2, Or(A9, Not(A2))))))  Or(A7, Not(Not(And(A2, Or(A9, Not(A2))))))
A9                                          A9
A12                                         A12
A2                                          A2
Impl(X2, A10)                               Impl(X2, A10)
Not(A3)                                     Not(A3)
A7                                          A7
Not(Not(And(A2, Or(A9, Not(A2)))))          Not(Not(And(A2, Or(A9, Not(A2)))))
X2
A10
A3
Not(And(A2, Or(A9, Not(A2))))
And(A2, Or(A9, Not(A2)))
Or(A9, Not(A2)) 

(Internal)      Context 1                                       (Internal)      Context 2
--------------  ----------------------------------------------  --------------  ----------------------------------------------
[]                                                              []
[0, 1, 2]       A1, And(A1, A2), Not(A2)                        [0, 1, 2]       A1, And(A1, A2), Not(A2)
[3]             Impl(A12, Not(A2))                              [3]             Impl(A12, Not(A2))
[4, 5, 6]       A4, Or(Impl(X2, A10), Not(A3)), A5              [4, 5, 6]       A4, Or(Impl(X2, A10), Not(A3)), A5
[1]             And(A1, A2)                                     [1]             And(A1, A2)
[7, 8]          Or(A7, Not(Not(And(A2, Or(A9, Not(A2)))))), A9  [7, 8]          Or(A7, Not(Not(And(A2, Or(A9, Not(A2)))))), A9
[9]             A12                                             [9]             A12
[0, 1]          A1, And(A1, A2)                                 [0, 2, 0]       A1, Not(A2), A1
[3, 10]         Impl(A12, Not(A2)), A2                          [0, 2, 10]      A1, Not(A2), A2
[0, 2, 0]       A1, Not(A2), A1                                 [0, 1, 2, 9]    A1, And(A1, A2), Not(A2), A12
[0, 2, 10]      A1, Not(A2), A2                                 [2]             Not(A2)
[0, 1, 2, 9]    A1, And(A1, A2), Not(A2), A12                   [0]             A1
[2]             Not(A2)                                         [10]            A2
[0]             A1                                              [4, 6, 11]      A4, A5, Impl(X2, A10)
[10]            A2                                              [4, 6, 12]      A4, A5, Not(A3)
[4, 6, 11]      A4, A5, Impl(X2, A10)                           [8, 13]         A9, A7
[4, 6, 12]      A4, A5, Not(A3)                                 [8, 14]         A9, Not(Not(And(A2, Or(A9, Not(A2)))))
[8, 13]         A9, A7                                          [0, 2, 0, 9]    A1, Not(A2), A1, A12
[8, 14]         A9, Not(Not(And(A2, Or(A9, Not(A2)))))          [0, 2, 10, 9]   A1, Not(A2), A2, A12
[0, 0]          A1, A1                                          [0, 1, 9]       A1, And(A1, A2), A12
[0, 10]         A1, A2                                          [0, 1, 2, 10]   A1, And(A1, A2), Not(A2), A2
[0, 1, 9]       A1, And(A1, A2), A12                            [0, 0, 9]       A1, A1, A12
[10, 2]         A2, Not(A2)                                     [0, 2, 0, 10]   A1, Not(A2), A1, A2
[0, 2, 0, 9]    A1, Not(A2), A1, A12                            [0, 10, 9]      A1, A2, A12
[0, 2, 10, 9]   A1, Not(A2), A2, A12                            [0, 2, 10, 10]  A1, Not(A2), A2, A2
[0, 1, 2, 10]   A1, And(A1, A2), Not(A2), A2                    [0, 1, 10]      A1, And(A1, A2), A2
[4, 6]          A4, A5                                          [0, 0, 10]      A1, A1, A2
[1, 15]         And(A1, A2), X2                                 [0, 10, 10]     A1, A2, A2
[4, 6, 16]      A4, A5, A10
[1, 17]         And(A1, A2), A3
[8]             A9
[9, 18]         A12, Not(And(A2, Or(A9, Not(A2))))
[0, 0, 9]       A1, A1, A12
[0, 10, 9]      A1, A2, A12
[0, 1, 10]      A1, And(A1, A2), A2
[0, 2, 0, 10]   A1, Not(A2), A1, A2
[0, 2, 10, 10]  A1, Not(A2), A2, A2
[0, 15]         A1, X2
[0, 17]         A1, A3
[10, 15]        A2, X2
[10, 17]        A2, A3
[8, 19]         A9, And(A2, Or(A9, Not(A2)))
[0, 0, 10]      A1, A1, A2
[0, 10, 10]     A1, A2, A2
[8, 10]         A9, A2
[8, 20]         A9, Or(A9, Not(A2))
[8, 8]          A9, A9
[8, 2]          A9, Not(A2)
[9, 10]         A12, A2 

(Internal)        Context 1                                                (Internal)        Context 2
------------  --  -------------------------------------------------------  ------------  --  -------------------------------------------------------
(0, 0)            |~LK                                                     (0, 0)            |~LJ
(1, 2)            A1, And(A1, A2), Not(A2) |~LK Impl(A12, Not(A2))         (1, 2)            A1, And(A1, A2), Not(A2) |~LJ Impl(A12, Not(A2))
(3, 4)            A4, Or(Impl(X2, A10), Not(A3)), A5 |~LK And(A1, A2)      (3, 4)            A4, Or(Impl(X2, A10), Not(A3)), A5 |~LJ And(A1, A2)
(5, 6)            Or(A7, Not(Not(And(A2, Or(A9, Not(A2)))))), A9 |~LK A12  (5, 6)            Or(A7, Not(Not(And(A2, Or(A9, Not(A2)))))), A9 |~LJ A12
(7, 8)            A1, And(A1, A2) |~LK Impl(A12, Not(A2)), A2              (7, 2)            A1, Not(A2), A1 |~LJ Impl(A12, Not(A2))
(9, 2)            A1, Not(A2), A1 |~LK Impl(A12, Not(A2))                  (8, 2)            A1, Not(A2), A2 |~LJ Impl(A12, Not(A2))
(10, 2)           A1, Not(A2), A2 |~LK Impl(A12, Not(A2))                  (9, 0)            A1, And(A1, A2), Not(A2), A12 |~LJ
(11, 0)           A1, And(A1, A2), Not(A2), A12 |~LK                       (1, 10)       *   A1, And(A1, A2), Not(A2) |~LJ Not(A2)
(1, 12)       *   A1, And(A1, A2), Not(A2) |~LK Not(A2)                    (3, 11)           A4, Or(Impl(X2, A10), Not(A3)), A5 |~LJ A1
(3, 13)           A4, Or(Impl(X2, A10), Not(A3)), A5 |~LK A1               (3, 12)           A4, Or(Impl(X2, A10), Not(A3)), A5 |~LJ A2
(3, 14)           A4, Or(Impl(X2, A10), Not(A3)), A5 |~LK A2               (13, 4)           A4, A5, Impl(X2, A10) |~LJ And(A1, A2)
(15, 4)           A4, A5, Impl(X2, A10) |~LK And(A1, A2)                   (14, 4)           A4, A5, Not(A3) |~LJ And(A1, A2)
(16, 4)           A4, A5, Not(A3) |~LK And(A1, A2)                         (15, 6)           A9, A7 |~LJ A12
(17, 6)           A9, A7 |~LK A12                                          (16, 6)           A9, Not(Not(And(A2, Or(A9, Not(A2))))) |~LJ A12
(18, 6)           A9, Not(Not(And(A2, Or(A9, Not(A2))))) |~LK A12          (17, 0)           A1, Not(A2), A1, A12 |~LJ
(19, 8)           A1, A1 |~LK Impl(A12, Not(A2)), A2                       (7, 10)       *   A1, Not(A2), A1 |~LJ Not(A2)
(20, 8)       *   A1, A2 |~LK Impl(A12, Not(A2)), A2                       (18, 0)           A1, Not(A2), A2, A12 |~LJ
(21, 14)          A1, And(A1, A2), A12 |~LK A2                             (8, 10)       *   A1, Not(A2), A2 |~LJ Not(A2)
(7, 22)           A1, And(A1, A2) |~LK A2, Not(A2)                         (19, 12)          A1, And(A1, A2), A12 |~LJ A2
(23, 0)           A1, Not(A2), A1, A12 |~LK                                (20, 0)           A1, And(A1, A2), Not(A2), A2 |~LJ
(9, 12)       *   A1, Not(A2), A1 |~LK Not(A2)                             (13, 11)          A4, A5, Impl(X2, A10) |~LJ A1
(24, 0)           A1, Not(A2), A2, A12 |~LK                                (14, 11)          A4, A5, Not(A3) |~LJ A1
(10, 12)      *   A1, Not(A2), A2 |~LK Not(A2)                             (13, 12)          A4, A5, Impl(X2, A10) |~LJ A2
(25, 0)           A1, And(A1, A2), Not(A2), A2 |~LK                        (14, 12)          A4, A5, Not(A3) |~LJ A2
(15, 13)          A4, A5, Impl(X2, A10) |~LK A1                            (21, 12)          A1, A1, A12 |~LJ A2
(16, 13)          A4, A5, Not(A3) |~LK A1                                  (22, 0)           A1, Not(A2), A1, A2 |~LJ
(15, 14)          A4, A5, Impl(X2, A10) |~LK A2                            (23, 12)      *   A1, A2, A12 |~LJ A2
(16, 14)          A4, A5, Not(A3) |~LK A2                                  (24, 0)           A1, Not(A2), A2, A2 |~LJ
(26, 27)          A4, A5 |~LK And(A1, A2), X2                              (25, 12)      *   A1, And(A1, A2), A2 |~LJ A2
(28, 4)           A4, A5, A10 |~LK And(A1, A2)                             (26, 12)      *   A1, A1, A2 |~LJ A2
(26, 29)          A4, A5 |~LK And(A1, A2), A3                              (27, 12)      *   A1, A2, A2 |~LJ A2
(30, 31)          A9 |~LK A12, Not(And(A2, Or(A9, Not(A2))))
(32, 14)          A1, A1, A12 |~LK A2
(19, 22)          A1, A1 |~LK A2, Not(A2)
(33, 14)      *   A1, A2, A12 |~LK A2
(20, 22)      *   A1, A2 |~LK A2, Not(A2)
(34, 14)      *   A1, And(A1, A2), A2 |~LK A2
(35, 0)           A1, Not(A2), A1, A2 |~LK
(36, 0)           A1, Not(A2), A2, A2 |~LK
(26, 37)          A4, A5 |~LK A1, X2
(28, 13)          A4, A5, A10 |~LK A1
(26, 38)          A4, A5 |~LK A1, A3
(26, 39)          A4, A5 |~LK A2, X2
(28, 14)          A4, A5, A10 |~LK A2
(26, 40)          A4, A5 |~LK A2, A3
(41, 6)           A9, And(A2, Or(A9, Not(A2))) |~LK A12
(42, 14)      *   A1, A1, A2 |~LK A2
(43, 14)      *   A1, A2, A2 |~LK A2
(44, 6)           A9, A2 |~LK A12
(45, 6)           A9, Or(A9, Not(A2)) |~LK A12
(46, 6)           A9, A9 |~LK A12
(47, 6)           A9, Not(A2) |~LK A12
(30, 48)          A9 |~LK A12, A2 
```