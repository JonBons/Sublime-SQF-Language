// Test SQF language constants
private _nil = nil;
private _true = true;
private _false = false;

// Test side constants
private _west = west;
private _east = east;
private _independent = independent;
private _civilian = civilian;

// Test other constants
private _pi = pi;
private _endl = endl;
private _linebreak = linebreak;

// Test in conditions
if (_true) then {
    hint "True constant works";
};

if (_west == west) then {
    hint "Side constant works";
};
