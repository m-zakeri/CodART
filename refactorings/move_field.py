"""
# Move Field Refactoring
Creates a field in a new class and redirect all users of the old field to it.
**Reference:** https://refactoring.guru/move-field

## Parameters:
- Source Class
-  Target Class
-  Field Identifier
## Pre-Conditions:
 1. Check existence of source class, Field, and the target class
 2. Check if there is no duplicate field
 3. Check if field is static, use the Move Static Field Refactoring
 4. No usages outside the source and target class  [Simple Solution]
## Algorithm:
 1. Pass Pre-Conditions
 2. Create an empty constructor in target class if not exists.
 3. Update usages ( Create new instance of target class)
## Post-Conditions:
 None
## Example:
```
 Class A, field Class B
 A a = new A(); // unused code [We can ignore or use dead code refactoring]
 B b = new B();
 int test = b.field + 22;
 ```

"""
