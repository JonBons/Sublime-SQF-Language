// Test illegal SQF syntax patterns
private _test = "valid string";

// Test illegal @ symbol
private _invalid = @invalid;

// Test illegal ? symbol  
private _question = ?invalid;

// Test illegal $ usage (not hex)
private _invalidDollar = $invalid;

// Test illegal | with spaces
private _invalidPipe = | invalid |;

// Test illegal . after identifier
private _invalidDot = identifier.invalid;

// Test illegal := operator
private _invalidAssignment = variable := value;

// Test illegal [: syntax
private _invalidBracket = [:invalid];

// Test valid hex numbers (should be legal)
private _validHex1 = 0xFF;
private _validHex2 = $FF;
