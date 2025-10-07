// Test code blocks with proper punctuation highlighting
if (true) then {
    private _inside = "inside block";
    hint "Block content";
};

while {_condition} do {
    private _loopVar = 0;
    _loopVar = _loopVar + 1;
};

// Test nested blocks
for "_i" from 0 to 5 do {
    if (_i > 2) then {
        hint format ["Value: %1", _i];
    };
};

// Test function blocks
call {
    private _localVar = "in function block";
    systemChat _localVar;
};
