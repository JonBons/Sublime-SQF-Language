// Test various number formats
private _decimal = 123;
private _float = 123.45;
private _scientific = 1.23e-4;
private _hex = 0xFF;
private _hexDollar = $FF;
private _hexLarge = $1A2B;
private _zero = 0;
private _negative = -42;
private _negativeFloat = -3.14;

// Test in expressions
private _result = 0xFF + $1A2B;
private _another = _decimal * _hexDollar;

// Test in function calls
hint format ["Hex value: %1", $FF];
hint format ["Decimal value: %1", 123];
