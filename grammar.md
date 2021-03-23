The nonterminals `expression` and `assign_expression` are unreachable in this version of the grammar

```
expression	            : assign_expression

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


declaration             : declaration_specifiers opt_declaration

declaration_specifiers  : PLEASE data_type ID

data_type               : INT
                        | FLOAT_T
                        | STRING_T

opt_declaration	        : ';'
                        | initializer ';'

initializer             : '=' eq_expression
```
