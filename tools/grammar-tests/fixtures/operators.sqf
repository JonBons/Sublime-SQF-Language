// Test comparison operators
private _result1 = 5 == 5;
private _result2 = 3 != 4;
private _result3 = 10 <= 15;
private _result4 = 20 >= 18;
private _result5 = 7 < 8;
private _result6 = 9 > 6;

// Test arithmetic operators
private _sum = 5 + 3;
private _diff = 10 - 4;
private _prod = 6 * 7;
private _quot = 15 / 3;
private _mod = 17 % 5;
private _pow = 2 ^ 3;

// Test in expressions
if (_sum > _diff) then {
    private _complex = (_prod * _quot) + (_mod ^ 2);
};
