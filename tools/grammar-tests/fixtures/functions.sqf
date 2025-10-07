// Test function naming convention
player call myTag_fnc_myFunction;
call anotherTag_fnc_anotherFunction;

// Test built-in functions
private _result = abs (-5);
private _distance = distance player target;
private _array = [1, 2, 3, 4, 5];

// Test function calls
hint format ["Result: %1", _result];
player setPosATL [0, 0, 0];
systemChat "Function test complete";

// Test custom function pattern
call myMod_fnc_customFunction;
call anotherMod_fnc_processData;
