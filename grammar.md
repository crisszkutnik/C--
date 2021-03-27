```
// Expressions

expression              : assign_expression

assign_expression       : eq_expression
                        | ID arr_access '=' eq_expression

eq_expression           : rel_expression
                        | rel_expresion EQUALS eq_expression

rel_expression	        : sum_expression
                        | sum_expression '>' rel_expression
                        | sum_expression '<' rel_expression

sum_expression          : mul_expression
                        | mul_expression '+' sum_expression
                        | mul_expression '-' sum_expression

mul_expression          : primary_expression
                        | primary_expression '*' mul_expression
                        | primary_expression '/' mul_expression
                        | primary_expression '%' mul_expression

primary_expression      : ID arr_access
                        | FLOAT
                        | INTEGER
                        | STRING
               
arr_access              : '[' eq_expression ']'
                        | empty

expression_list         : eq_expression ',' expression_list
                        | eq_expression

// Declarations

declaration             : PLEASE declaration2

declaration2            : var_declaration
                        | list_declaration

list_declaration        : LIST ID opt_list_declaration

opt_list_declaration    : '=' '[' expression_list ']'

var_declaration         : declaration_specifiers opt_declaration

declaration_specifiers  : data_type ID

data_type               : INT
                        | FLOAT_T
                        | STRING_T

opt_declaration	        : ';'
                        | initializer ';'

initializer             : '=' eq_expression

// Sentences

sentence                : compound_sentence
                        | decision_sentence
                        
compound_sentence       : '{' '{' code_block_list '}' '}'

decision_sentence       : PLEASE IF '(' eq_expression ')' DO compound_sentence else_statement

else_statement          : ELIF '(' eq_expression ')' DO compound_sentence else_statement
                        | ELSE DO compound_sentence
                        | empty

// Code structure

program                 : code_block_list
                        
code_block_list         : code_block code_block_list
                        | empty
                        
code_block              : declaration
                        | expression ';'
                        | sentence
```
