The nonterminals `expression` and `assign_expression` are unreachable in this version of the grammar

```
// Expressions

expression              : assign_expression

assign_expression       : eq_expression
                        | ID '=' eq_expression

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

primary_expression      : ID
                        | FLOAT
                        | INTEGER
                        | STRING


// Declarations

declaration             : declaration_specifiers opt_declaration

declaration_specifiers  : PLEASE data_type ID

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

decision_sentence       : IF '(' eq_expression ')' compound_sentence

// Code structure

program                 : sentence
                        | code_block_list
                        
code_block_list         : code_block
                        | empty
                        
code_block              : declaration code_block_list
                        | expression ';' code_block_list
```
