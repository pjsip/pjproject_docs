Coding Style
======================
If you intend to submit patches to PJSIP, please be informed that we do have the following
coding style. Please do not see this as something that we guard religiously, but
it's just **the** conventions that has been established for the past couple of decades in the
existing hundreds of thousand lines of code and we think it's just nice if new codes could follow these
conventions.


.. contents:: Topics:
   :local:
   :depth: 2


Space indentation
-----------------------
Indent by 4 characters and **use spaces only**.

The PJSIP distribution includes an :source:`.editorconfig` file to set indentation to 
4 spaces. Check https://editorconfig.org/ to see if your editor supports it or
if a plugin needs to be downloaded.

.. note::

   PJSIP indentation scheme was changed to use spaces only since version 2.13.


Limit line length
-----------------------
We usually limit the line length to 80 characters, especially in the header files.
A few violations in the ``.c`` file are usually tolerated, especially in the test files
where the audience is limited, but usually they are less than 90 characters too.


Use ANSI C/C90 Standard
--------------------------
Our code is ANSI C (a.k.a C89, C90, ISO C) plus allowing C++ ``//`` style comment for **special
occasion** (see next section). In some compilers this is called ``gnu89``, and
in **gcc** you can activate this with ``-std=gnu99`` option.



Use C style comment
---------------------
Use C style comment. We only use C++ ``//`` style comment when we want some part of
disabled code to draw more attention than normal comment, and as a reminder in the
future that we used to have that code (and it was disabled for a reason). For example:

.. code-block:: c

    /* Everything is fine, this is just a normal comment */
    i += 1;

    // This code is suspicious, I'm disabling it until further investigation
    // *(int*)0 = 0;


No declaration after statement
----------------------------------
We don't use declaration after statement because our compiler did not support it back then
(even Visual Studio 2005 still did not support it) and this is not allowed by C90 (or so we thought).

.. note::

    But somewhat it is allowed by current ``gcc -std=c90`` and ``gcc -std=gnu89``,
    though you can get gcc to warn you about it with ``-Wdeclaration-after-statement``.

We would appreciate if you could avoid it too.


Use Doxygen comments for API
------------------------------
All public API in header file must be documented in Doxygen format. This includes structs, enums,
and their members, functions, their arguments, macros, etc.

Please see example in the next section on how to indent the comments.


Use K&R style brace placement
--------------------------------
Braces are on their own lines for **function, struct, and enum definitions**:

.. code-block:: c

    /** Doxygen comment */
    typedef struct some_type
    {
        /** Doxygen comment */
        int   member_a;

        /** Doxygen comment */
        char  member_b;
    } some_type;
    
    /** Doxygen comment */
    enum some_constant_t
    {
        /** Doxygen comment */
        CONSTANT_1,

        /** Doxygen comment */
        CONSTANT_2;
    };

    /**
     * Doxygen comment describing the function.
     *
     * @param a     First parameter
     * @param b     Second parameter, same indentation as other params.
     *
     * @return      Zero on success or ..., indentation aligned with above too.
     */
    int my_func(int a, int b)
    {
        return 0;
    }

For other blocks, opening braces are on the same line, except if the statement preceeding the
braces is multiline

.. code-block:: c

    for (i=0; i<count; ++i) {
        ...
    }

    /* multiline example */
    while (imagine_long_expression_here > 0 &&
           another_condition_is_true)
    {
    }



Please observe existing code
------------------------------
Those are the main things about coding style that we wish new code would follow.
This document will be too terse if we have to mention all the little bits about style.
For everything else, please observe existing codes and adjust the style accordingly.
