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

decision_sentence       : PLEASE IF '(' eq_expression ')' DO compound_sentence else_statement

else_statement          : ELIF '(' eq_expression ')' DO compound_sentence else_statement
                        | ELSE DO compound_sentence
                        | empty

sentence_code_block     : declaration sentence_code_block
                        | expression ';' sentence_code_block
                        | sentence sentence_code_block
                        | empty

// Code structure

program                 : code_block_list
                        
code_block_list         : code_block code_block_list
                        | empty
                        
code_block              : declaration
                        | expression ';'
                        | sentence
```
