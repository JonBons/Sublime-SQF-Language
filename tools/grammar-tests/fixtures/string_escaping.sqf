// Test string escaping functionality
hint "Hello ""World""!";
hint 'Hello ''World''!';
hint "This is a ""quoted"" string with ""multiple"" quotes";
hint 'This is a ''quoted'' string with ''multiple'' quotes';

// Test regular strings without escaping
hint "Regular string";
hint 'Regular string';

// Test mixed content
hint "Player ""John"" has score: " + str 100;
hint 'Player ''Jane'' has score: ' + str 200;
