:version: $RCSfile: design-principles.rst,v $ $Revision: efffb0e4678e $ $Date: 2010/11/09 16:11:51 $

.. default-role:: fs

.. _design-principles:

================================
 Some Issues in Software Design
================================

:date: June 16, 2007

.. contents::
   :local:

.. _software-design-principles:

Software design principles
==========================

The software at this site was written with the following engineering
design principles in mind:

+  **Simplicity: as simple as possible but no simpler.**
   (That is a paraphrase of a statement attributed to Einstein about
   physics.) *The most simple methods are used that do not significantly
   sacrifice performance*.

   + If it would take 1000 lines of code to double the performance of a
     20 line algorithm, forget it; we'll use the 20 line method.

   + If the simplest efficient method is a bit tricky, as with a general
     implementation of rasterops, so be it.

+  **Efficiency.** This is the yin to the yang of simplicity. The goal is
   to have the algorithm be both simple and efficient. Data is handled
   32 bits at a time whenever possible. But there is often room for
   improving efficiency if the need exists. For example, I generate and
   use 8-bit lookup tables throughout, but given the large size of
   caches in current systems, 16-bit tables are more efficient.

+  **Clarity.** I attempt always to make the method clear. The goal is to
   allow a C programmer to read the source, and any associated
   information, and understand exactly what is happening. Comments are
   placed in the code so that the method can be quickly understood. The
   naming convention in the higher-level code is object-"oriented". The
   function name starts with the primary object being operated on or
   being returned.

+  **Portability.** I attempt to make the software as portable as
   possible. This has several aspects:

   +  Written in C. (Also for efficiency and simplicity.)

   +  *A low-level implementation*, using only intrinsic C data types, that
      is (almost) independent of the application-level image data
      structures, is (almost) always split out from the higher-level
      code.

   +  There are two requirements on the image data array of the
      application-level image data structure:

      #. The array must be in a single consecutive block.

      #. Each raster line must start on a 32-bit word boundary.

   +  A simple image data structure is used to (informally) verify
      correctness and show how to use the lower-level functions. In some
      cases, such as rotation by shear, the details of the algorithm are
      mostly in the higher-level code.

   +  Endian independent.

   +  Typedefs for intrinsic data types that can easily be changed and are
      written to avoid conflicts with other libraries.

   +  Use of macros for common operations, e.g. allocation of heap memory,
      where programmers often want to make substitutions determined at
      compile time.

+  **Code safety.** This may seem like an oxymoron when applied to C, but
   there are several things that do help in the higher-level code. The
   emphasis is on safe memory allocation and deallocation, avoiding
   references through null pointers, and (optionally) giving useful
   debugging information when something goes wrong. A little work to
   prevent the library from crashing applications more than makes up for
   all the time users of the library would have spent mucking around in
   :cmd:`gdb`. You may find the code heavy on checks of variables and
   function returns, but the alternative is worse.

   +  Do all memory allocation in higher-level code.

   +  Check all pointers passed to higher-level code functions.

   +  Check return values; in particular, for pointers to allocated data.

   +  Usually allocate arrays and data structures on the heap, either
      returning them or destroying them before the function returns.

   +  Use accessors for fields in high-level data structures, that check
      the pointer value before the access.

   +  Provide ``create()`` and ``destroy()`` functions for all data
      structures.

   +  Avoid globals, including statics, except for constants.

   +  Require each calling function to clean up all arrays that it is
      responsible for allocating and that are *not* put in a data
      structure.

   +  Use a mechanism, selectable at compile time, that gives a trace of
      the call stack when a test for memory allocation or access fails.

   +  Make evident which function is responsible for destroying each data
      structure. This is most easily arranged by requiring the function
      that calls ``create()`` for a data structure to call ``destroy()``
      on it. Sometimes this is not convenient. For example, you may have
      an ``init()`` function that calls ``create()`` and a ``cleanup()``
      function that calls ``destroy()`` on a number of data
      structures. Another example is when you create a structure and add
      it to an array of pointers to similar structs. If you add it by
      insertion (of the pointer), the protocol is that it is now owned
      by the array, and the function that destroys the array takes care
      of it. In the first example, some higher-level function is
      required to call both ``init()`` and ``cleanup()``. In all cases,
      *it is important to have a sensible, consistent and documented
      protocol*.

   +  Never call ``exit()`` from a library.

Marin Saric recently pointed me to Robert Glass's "Facts and Fallacies
of Software Engineering," Addison-Wesley, 2003. Of the many "Facts" in
that book, the most interesting I found were on the life cycle of
software. Considering the five stages (*requirements*, *design*,
*coding*, *error removal* and *maintenance*), maintenance occupies about
60 percent of the total (Fact 41). Further, about 60 percent of
maintenance is for enhancements, as opposed to bug fixes --- "software
maintenance is largely about adding new capability to old software, not
fixing it." (Fact 42). And then the kicker: "Better software engineering
leads to more maintenance, not less." (Fact 45). Better software is
better structured and easier to understand and modify. It encourages
modification. So Glass can conclude that maintenance is a solution, not
a problem (Fact 43).

There are many other gems in this book, describing, for example, the
disconnect between engineers and managers, the problems with
schedule-fixing and subsequent changes in requirements, the problems
that arise when the designers don't do the coding, the absence of
updated design docs or retrospective design descriptions that would help
people maintain the software, the lack of a silver bullet for building
reliable software, and the various methods that have been used for
removing errors. (One of the best such methods is rigorous
inspection --- Fact 37).

Glass says that quality is a collection of attributes. His seven
"-abilities", not in any particular order, are *portability*,
*reliability*, *efficiency*, *usability*, *testability*,
*understandability* and *modifiability*. I found this interesting
because they are the same requirements I have informally put on
Leptonica. To mention three, I have put some effort into
"understandability," both with comments within the code and with web
pages describing the problem addressed and its applications, the
algorithms used, and the resulting functionality, sometimes going down
to the actual form of the functional interface. This documentation helps
me (and others) modify the code. Because the Leptonica library is a
programmer's interface, "usability" and "portability" go together to
some extent; for example, the separation between high-level code that
uses simple data structures and low-level code that uses only built-in C
data types, and the use of a very simple data structure for generic
images.  Further, the definition and re-use of a small number of data
structures simplifies the application of the Leptonica library to
various problems. And the various constructs and patterns I use to catch
errors and prevent program crashes contribute to both reliability and
usability. These are discussed in more detail above.

Other recommended reading: Butler Lampson's :unconverted:`Hints for
Computer System Design <cachedpages/lampson-hints.html>`. This is a
distillation of lessons learned by the graybeard of the Xerox PARC
pioneers.


What happens when things go wrong?
==================================

What is a library?

Description 1:
   A library is a set of abstractions that should allow you
   to get the information you need without sweating all the low-level
   details. For image processing, those "low-level details" are often
   relations between pixel values.

Description 2:
   A library is a set of functions that typically (but not always) take
   a set of inputs and generate a set of outputs. (If the function
   doesn't give you anything back, why would you ever run it?) Look at
   the description of the function. It typically says what you need to
   provide and what you get in return. It should also specify any
   constraints on the input.

Description 3:
   A library is a set of contracts: "If you give me *this*, I will give
   you *that*." That's the explicit part. But there is more to the
   contract than what goes in and what comes out. There is a very
   important implicit part that governs:

   + *ownership*: Who owns any stuff that is allocated?

   + *side effects*: What are you allowed to do to the input? Are
     globals or static variables being modified?

   + *error handling*: What happens when an error occurs?

   + *integration*: What issues may come up?

With all of these, the contract should have a default condition
throughout the library, and any deviations from the default need to be
noted in the function description.

We've discussed ownership, side effects and some of the integration
and portability issue in the previous section. For example,
portability is enhanced by using POSIX library functions, being
careful with function, typedef and global constant names to avoid
namespace clashes, and using endian-independent implementations. Here,
I want to say a bit about error handling.

What to do when an error occurs is a vexing problem because users will
want the behavior to be anything from "crash immediately if an error
occurs" to "just carry on, I expect errors because I have errorful or
highly variable input and may not want (or be able) to test for
abnormal conditions at each point." The degree to which the input and
processing actions are constrained in the application is crucial. For
image analysis applications, there is often sufficient uncertainty and
variability in the image content that the programs will need to handle
unanticipated situations. There is little I find more annoying than
using a library where a function crashes the application by calling
exit on error. Leptonica is guaranteed *not* to do that, *ever*.

Some languages like Java have error handling primitives (try, catch)
built in. Because C is more primitive and low-level, error handling is
done in an ad hoc manner of the library designer's choosing.

The user's needs can vary depending if you're in a development
environment (e.g., "unwind the call stack with appropriate messages")
or in production (e.g., "crash so I can figure out what went wrong" or
"go on, but don't show me a lot of debug messages"). The library
should be able to accommodate all these different ways of handling
errors. It should also be reasonably good about cleaning up garbage
when a function ends prematurely.

Another option in the user's implementation is whether or not to make an
effort to inspect all returned objects and to explicitly say what to do
in each case. For robust applications, it is desirable to check returned
values to determine if an error has occurred. But this should be a
programmer decision, and, in particular, the library functions should be
written in such a way that *an application should not crash if it
continues after an error*. It is obvious that the library function
should not corrupt (or lose) memory, no matter what. But at the
application level, how does the library prevent a crash? In general, of
course, it can't with a language like C where there is access to
pointers.

At the application level, most crashes are due to dereferencing an
invalid pointer. Leptonica allocates nearly everything on the heap, so
there are plenty of pointers being passed around. Leptonica data
structures are initialized with ``calloc``, so that all pointers in a
struct are automatically set to NULL. Accessors are provided so that the
programmer has no excuse to reference a field directly (and thereby
possibly dereference a null pointer).

A tricky place is where a function returns a pointer to a struct that
it allocated. The pointer itself is typically allocated on the stack,
uninitialized, by the calling function and then its address passed in
to the function that allocates the struct. An example should make this
clear:

.. sourcecode:: c

   ...
   Pix *pix = NULL;
   Pixa *pixa;  // ptr allocated on stack but not initialized

       // Heap allocated pixa should be returned, but in this case
       // because pix == NULL, pixa doesn't get allocated.
       // Suppose it is not initialized in the function.
   Boxa *boxa = pixConnComp(pix, &pixa, 8);
   ...
   Pix *pixt = pixaGetPix(pixa, 0, L_CLONE);  // segfault

The function can fail to do the allocation if it returns early. In the
code above, ``pixConnComp()`` returns immediately because ``pix`` is
NULL.  What about ``pixa``? It is never allocated, but if it is not
initialized before ``pix`` is tested, it will retain its random
value. In that case, any use is almost certain to crash the
program. Note that if the program were written to catch the error by
testing the returned ``boxa``, an uninitialized ``pixa`` should never
cause trouble. If ``pixConnComp()`` does early initialization, the
program won't crash under any circumstances.

The goal is thus to provide a programming environment with C library
functions that is as close as possible to the runtime safety of an
interpreter (like Matlab). Leptonica supports various options when an
error occurs --- crash immediately, give an error message and return
from the function, return silently --- by using error handling macros
throughout. By default, these print the name of the calling function
with an error message, and return with some value cast to the return
type of the function.


Extremism in programming languages
==================================

Most EE/CS students get an introductory course that compares programming
languages. Here, I present a somewhat biased summary of the extreme
features of programming languages, with a bit of history thrown in. We
start by noting that *extremism is the rule, not the exception, in
programming languages*.

Whereas compiler design is an engineering discipline (in fact, an
offshoot of discrete mathematics), the design of programming languages
is an art form, notwithstanding nearly 50 years of intense
experimentation. There is no manual or set of rules that tell you how to
design a language. The languages that have been designed and used
display a wonderful diversity, but most of the ones that are well-known,
if not widely used, take some characteristic to extremes. This might
seem puzzling: why are the best known languages typically *pure* in some
aspect rather than amalgams of methods that have been shown to be
generally useful?

Let's consider some examples. Xerox PARC developed three different
programming environments in the 1970s. These were all optimized to run
on the same bit-sliced 16-bit hardware, using microcode that defined
the basic machine operations for each of the three systems. The three
languages used were Lisp, Smalltalk and Mesa/Cedar. Each of the three
systems was written in the programming language and supported only
programs written in that language.

*Lisp* is an extreme language because *it has the most simple syntax
invented: everything is a list*. Unless the list is "quoted," which
means to take it literally, the first element is an operation and the
remaining elements are data to be acted on. The parser for Lisp needs to
identify only parenthesis and quote signs, and evaluate the expressions
from the inside-out. Lisp is also extreme in that no data in Lisp needs
to be explicitly typed. (It shares this characteristic with most
scripting languages, where typing is done implicitly.)

*Smalltalk* is an extreme language because *it has the most uniform set
of datatypes invented: everything is an object*. Even the integer 3 is
an object. All objects have data and functions associated with them.
(The Smalltalk inventors called procedures that act on objects
"methods", thus overloading yet another common word.) The objects are
arranged in a hierarchy that allows subclassing with inheritance of data
and functions from above.

Unlike Lisp and Smalltalk, *Mesa/Cedar* was extreme in that it was
strongly typed. You could defeat the typing, but it took more than a
simple cast and was heavily discouraged, requiring something like
signing your name in blood to the deprecated code. The strong typing was
necessary because Mesa/Cedar shared one fundamental aspect with Lisp and
Smalltalk: *all functions ran in the same memory space as the operating
system!* This in itself was an extreme decision, because a poorly
written piece of code in Mesa/Cedar could bring everything down. Lisp
and Smalltalk were languages that were meant to be interpreted, and the
designers absorbed protection against memory smashes into the
inefficiencies that naturally come with interpreters.  But Mesa/Cedar
was meant to be an efficient language and programming environment, with
optimizing compilers; no runtime cycles were to be wasted checking
memory accesses. Hence the requirement for strong typing. Mesa also
incorporated another safety feature of Lisp and Smalltalk: garbage
collection. You couldn't afford to have programmers messing with dynamic
memory allocation! And because of the strong typing, garbage collection
was a relatively straightforward engineering task. (As an interesting
comparison, the line of Microsoft operating systems including Windows
3.1, 95, 98, and 98SE, which were sold until 2001 when XP was
introduced, had neither pre-emptive multitasking nor memory protection
to encapsulate the addressing of applications. Consequently, any
application could hang or crash the entire system. In view of the fact
that, with Unix, people knew how to design an operating system over 30
years ago that was protected from bad behavior by user-level processes,
and further, we have had on-chip hardware memory protection since the
mid 1980s (e.g., in the Intel 80386 and Motorola 68020), this seems to
be a very strange way to design system software.)

Most of the other languages have had extreme characteristics. *C*, the
most successful language ever developed, is extreme in its minimal
number of operations and built-in data types, and in its close
relationship to machine operations. Its minimality is in sharp to
contrast to Pascal, which incorporated into the language many of the
several hundred functions that C includes through libraries. The
oft-heard disparagement that C is an "assembler language" is an example
of the extreme positions that programmers often take. In fact, C has no
control of registers and supports manipulations on arbitrarily complex
data types.

*Forth* is extreme in that it uses an explicit stack. Whereas many other
languages have interpreters or compilers that use stacks internally,
Forth requires the programmer to push and pop every piece of data to and
from a stack, and, worse, *to remember exactly what is on the stack at
all times*. There is an advantage for the designers of Forth in putting
all this mental effort on the programmer: the interpreter is trivial; it
just maintains the data on the stack. Another disadvantage of this
simplicity is that source-level debuggers are (to my knowledge) unknown;
if something goes wrong, the most you get is a description of the stack
at that moment. PostScript is another example of a pure stack-oriented
language, but, of course, PostScript was never designed as a programming
language. The only things that the PostScript designers ever intended to
be written in PostScript were print and display drivers for specific
output devices.

The list goes on. Does anyone remember *prolog*? Prolog was extreme in
that it was intended for "predicate logic" programming: each statement
defined some logical relation between variables, and the interpreter
treated these relations as rules from which it would try to develop
other connections using boolean logic. This was an example of
*declarative programming*, as opposed the usual method where the
programmer tells the machine what to do. Logic programming was used for
special applications such as theorem-proving and so-called "AI expert
systems." Several AI proponents, notably Feigenbaum at Stanford,
proclaimed in hysterical writings in the late 1980s that Japan was going
to use prolog to build a "Fifth-Generation" computer that would be so
"smart" that it would wipe out the high tech industry in the United
States within five years. (Of course, he was trying to get more funding
for his own AI projects.) After five years, with the Fifth-Generation
project a complete failure, it appeared that prolog was merely a French
plot to retard the advance of Japanese technology.  Predicate logic
programs have been used with great success in Mathematica (and its
predecessors) to solve difficult problems in mathematics. This is
programming by pattern-substitution: you put in rules, such as "if you
see a pattern that looks like *this*, do *that*." With such methods, for
example, you can use Mathematica to get a closed-form expression for any
integral you can find in Gradshteyn and Ryzhik's monumental book *Tables
of integrals, series and products*!

And then there is *ML*, which used to be popular in Scotland, at least.
ML is an extreme programming language because there are *no side
effects*. Lisp programming practice might tend in this direction, but in
ML, it's the law. The way I visualize an ML program is that procedures
get called by other procedures ad infinitum, but everything returned is
just input to another function --- think of the data as always coming
back onto the stack that holds input variables for the next function
call. At the end, when the music stops, you find that nothing remains of
all the activity. I've been told that one of the trickiest programming
tasks in ML is to write a for-loop iterator, perhaps because it needs to
keep some state around to test for exit. I hope someone will explain to
me the allure of the extremism in the design of ML.

We're not finished yet. Scripting languages, of which *Perl* is the best
known, are extreme in that all data is treated as strings, with
arithmetic data being typed implicitly. Efficiency is sacrificed for
ease of use. These languages do more than use pattern matching to
manipulate strings. They have been extended to invoke programs, like a
shell script on steroids. Perl had the lucky timing to be on the scene
in 1995 for the WWW revolution; consequently, it has been the most
common scripting language used for server-side CGI web applications.

*Python* is another scripting language that has no data typing. It is
much more powerful than Perl, because it has objects, inheritance, the
Tk X graphical display library, and a very large number of application
modules to handle the interface to everything from databases to internet
applications. Python is extreme in its typographic minimalism. The
parser relies on typographic appearance: white space is an integral part
of the syntax. Python enthusiasts paraphrase Sierra Madre, "We don't
need no stinking braces," because scope and nesting is determined by
indentation alone! And there are no semicolons, because statements do
not carry over between lines. This is opposite to most languages, which
ignore white space entirely (including newlines). Python can be extended
with function calls to procedures compiled from other languages (e.g.,
C, C++). It is the most interesting scripting language, in terms of
simplicity and capability, yet invented.

Even *C++* is extreme in a particular way: while maintaining the
constraint of including C as a subset, C++ adopted nearly every
object-oriented programming feature known to man, including multiple
inheritance. It is thus extreme in its "kitchen-sink" approach to a
programming language. Additionally, C++ allows operator overloading.
This is illustrated by the canonical "cute" example of complex
arithmetic. However, it lends itself to very serious abuse because the
apparent syntax of the language can be changed at will. And
unfortunately it often is, making it very difficult to understand what
is actually happening. This is similar to the competitive stunts people
have done with the macro capability of the C preprocessor; however, with
C++, programmers do this for real. Another piece of syntactic sugar is
the automatic invocation of constructors, which can lead to extra
copying and inefficiencies if the programmer is not very careful.

*Java* is even more recent, and is the first serious programming
language that is, in my opinion, not extreme. (Well, it is extreme in
that all procedures are "methods" of an object; you cannot write a
function that is not within the file and scope of some object, even if
that object would never be instantiated.) It has a carefully selected
set of built-in features from C and C++, plus aspects that one finds in
interpreted languages, such as a byte-code generator with a byte- code
interpreter, automatic memory management, and threads.  (Interestingly,
byte-codes, automatic garbage collection and lightweight processes were
all included in Xerox's Cedar.) Java thus is an attempt to make a
language that takes the best features of C++, leaves the worst (operator
overloading, multiple inheritance), and adds new safety features
(garbage collection) and a byte code compiler for portability and safety
in web applications. Like Python, it is distinguished by having a very
large library of functions for doing application and systems
programming. Microsoft considered it to be a sufficiently dangerous
framework for non-Microsoft applications that they went to great lengths
to prevent it from working on Windows. Thanks, Bill.

The psychological basis of extremism in programming is very simple:
people crave simplicity and equate it to beauty and truth. In the
early days, when the engineering principles of compilers were in a
rudimentary stage, it was also good engineering to design a system
with a simple parser. With today's compiler building tools, such as
lex and yacc (or flex and bison), it is not difficult to build an
interpreter/compiler for a language such as C, so there is no excuse
for putting a lot of bookkeeping baggage on the back of the
programmer. But compilers for a language as large as C++ have proven
to be difficult to build, and some recently released versions of the
GNU g++ compiler (e.g., 2.96) have been buggy.

This is all an example of **Bloomberg's Law of Complexity**, which
paradoxically stands in firm opposition to the psychological desire for
simplicity and elegance: *the state of technology at any time is as
complicated as it possibly can be and still mostly work*. This explains
the ever-increasing complexity of languages like C++ and operating
systems like Windows. A corollary to the law of complexity is: *if
something can be added, it will*.

.. Note:: Historical note on limits of extremism

   In the late 1980s, when Xerox saw that its power-hungry homemade
   GaAs-based Dorados could not keep up with low-power commercial
   CMOS-based microprocessors, the Cedar runtime was ported to other
   hardware (e.g., SPARC), thus allowing Cedar to run as a single large
   process under Unix. The Cedar runtime supported the lightweight
   threads, that were invisible to the underlying OS. To maintain
   efficient operation, the port was done by compiling the Cedar/Mesa
   code to C, and then using the native C compiler. This was part of the
   unraveling of the short-lived age of monolithic computer
   environments. Years earlier, Peter Deutsch ported Smalltalk to the
   68010-based Sun2 (by writing a virtual machine in C to emulate the
   virtual machine previously implemented directly on hardware by
   microcode), thus paving the way for the ParcPlace spinout.  A similar
   approach was taken later to port the Xerox CommonLisp system to Suns,
   in a last-ditch effort to commercialize Xerox's Lisp programming
   environment.

   It is instructive to read the 1990 "Worse is Better" essay by Richard
   Gabriel, who founded *Lucid*, one of the Lisp-based computer makers
   that appeared in the 80s. With the collapse of the AI bubble, the
   unsuitability of Lisp systems to do most computing tasks became
   evident. Gabriel reluctantly admitted that "Worse" (i.e., the C
   language and the New Jersey-based Unix OS) was in fact "Better" for
   most things than the Boston-based Lisp. You can read just the
   :unconverted:`salient <cachedpages/worse-is-better-salient.html>`
   part of the argument, or Gabriel's introduction to his `musings and
   confusions <http://www.dreamsongs.com/WorseIsBetter.html>`_ over a
   10-year period on the "Worse is Better" theme. I find it most
   interesting that the almost religious extremism that Gabriel and
   others advocated in their monolithic creations blinded them to the
   power of an OS like Unix that is non-sectarian, and will support
   programming in many different styles, and with many different runtime
   systems, all simultaneously. They insisted on having pure Lisp all
   the way up and all the way down. Read Gabriel's essays to glimpse the
   degree to which smart people can become confused when the world just
   doesn't want their perfect creations. Extremism may prevail for
   programming languages with specific applications, but it is a
   disaster for the operating system.

   Yet another aside: if you want to read about one of the most ingenious
   computer hacks ever made, see Ken Thompson's `address on receipt of the
   1983 Turing Award <http://www.acm.org/classics/sep95/>`_, "Reflections
   on Trusting Trust", *Communications of the ACM* **27, 8**, Aug. 1984,
   pp. 761-763. Thompson managed to put a back-door into the login function
   to allow him to logon to Unix without an account, and he did this
   without leaving any evidence in the source code of either the operating
   system or the compiler! Here's what he did. He first made a compiler
   with the back-door, so that (1) if it compiled the OS, it would
   recognize the login function and insert the back-door, and (2) if it
   compiled the compiler, it would insert the code for producing the
   back-door. He then removed the back-door code from the source of the
   compiler. But the back-door was still there, hiding in the compiler
   binary, ready to replicate itself in any newly compiled compiler and to
   insert a back-door in any compiled OS. Hence the subject of his talk:
   what does it mean to "trust" in this multi-layered world of software?


Some practical issues in programming
====================================

I highly recommend Kernighan and Pike's *The Practice of Programming*.
This is a book for anyone who spends a lot of time programming, wonders
why so much code is so bad, and wishes not to contribute to the
problem. K and P have a three page appendix that is a collection of
rules, starting with a quotation by Descartes from his *Le Discours de
la Méthode*, which reads,

   Each truth that I discovered became a rule that served me afterwards
   in the discovery of others.
   
In engineering, a set of rules would suffice. But programming is not
sufficiently constrained by any known set of rules. For the "practice"
or "art" of programming, you also have to decide when to use the rules.

One of the things I've noticed is that people tend to use lists even in
situations where arrays are preferable. Here are my "rules" for lists
and arrays:

+ **Use arrays for queues and stacks.** When elements are only being
  added or removed from the beginning or the ends of a set of items,
  arrays are simpler and faster. The ``realloc`` C library function can
  be used to extend a dynamically allocated array, when necessary, using
  a size doubling rule. The array should be packaged in a structure (or
  class) that hides all details from the programmer. For example, stacks
  and queues are easily implemented for general objects using an array
  of ``void*`` pointers. In general, use arrays for data that doesn't
  change much, even if elements are occasionally added to or removed
  from the interior. When an item is removed, rather than moving an
  entire block of items upward, in some cases it's better to mark the
  item "invalid."

+ **Use lists when objects are routinely inserted into an ordered
  set**. With arrays, a random insertion causes movement of items that
  scales with the size of the array, whereas insertion into a list is
  independent of the list size as long as you know which items you're
  inserting between. (For a singly linked list, this requires knowing
  the item you insert *after*.)

+ **If you have to use a list, use a doubly-linked one**. Doubly-linked
  lists are a bit more expensive, but they allow the list to be
  traversed in reverse order. Once you've decided on doubly-linked
  lists, the next question is: should they be circular? I've found that
  circular doubly-linked lists work well but they're a lot more trouble
  to code up properly, so that elements can be added and removed at
  arbitrary places without breaking anything. David Kahn at `Perquest
  <http://www.perquest.com/>`_ first showed me how to use C macros to
  handle doubly-linked lists that are inserted as the first two pointers
  ("next" and "prev") directly in data structures. This configuration
  neatly sidesteps most issues with C typing, but one of the
  difficulties with inserting pionters directly in the data structures
  is that if you have a structure in a list and you insert a clone
  (which, after all, is just the same data structure) in another list,
  you will break the first list! Further, the macros for circular lists
  are fairly complicated, so I decided to do something much simpler in
  Leptonica, that would allow clones to be inserted in lists without
  problems. Without using macros, I made a doubly-linked but
  non-circular list utility that handles "cons" cells that hold data
  structures. One argument for using circular lists is that it takes no
  time to find the tail (the head typically points to it). However, if
  you're going to repeatedly access (or change) the tail, it's best to
  find it once and then be able to use it in the accessors. See `list.c`
  for some ideas for doing this.

.. _memory-management_issues:

Some issues with memory management
==================================

The biggest headache for C programmers is memory management. With C,
you have to make sure that you free all allocated memory, and also
that you do it exactly once for each allocated block. People have
built garbage collectors for C, but the usage rate is insignificant
because they do not work flawlessly. The problem is with C itself. You
can cast anything to void or to anything else. You can move the
pointer to an array by an arbitrary amount so that it points anywhere
within the address space relative to the beginning of the array. It
can even point outside the data segment as long as you don't access
it.

.. _valgrind-information:

But the best news in a long time for GNU C/C++ programmers is the
availability of a high quality open source memory management debugger
for x86/Linux called `valgrind <http://valgrind.org/>`_. Written by
Julian Seward, valgrind has essentially all the functionality of
:cmd:`purify`. But whereas purify works by re-writing the machine
instructions to capture information about memory accesses, Seward
circumvents the purify patents by instead running the program unaltered
on a *virtual machine* that does all the memory checking. That makes it
a bit slower, but you don't need to generate a whole set of
"purificated" libraries.

:cmd:`valgrind` is simple to use, without any change in your
program. You simply call::

   valgrind [valgrind args] your-program [your-program args]

I predict that the availability of valgrind will make significant
improvements in the quality of open source code. For example, when you
run valgrind with the png library, it finds memory access errors. And
there are so many errors with the GNU C library that Seward provides a
special suppression file containing errors that are not to be flagged!

Of course, it's better not to make the memory errors in the first
place. Above, I've given some of the :ref:`design principles
<software-design-principles>` on how memory can be managed in relatively
safety. One basic idea is to *replicate* the data when needed, such as
if you must embed some instance of a structure in more than one data
structure. The alternative is to rely on access to the same instance
from different places in the software, and you may force the application
programmer to remember who owns what and in what order allocated data
should be collected. This is generally bad practice, because it
complicates the use of the library and invites serious error. With
replication, each user of the data can have their own copy, for which
they are responsible.

Replication, however, can be expensive, particularly when you are
copying large structures like images. The simplest solution to this
problem is reference counting. For image and box data structures, I
allow multiple handles to the same data, with a reference count within
the ``PIX`` and ``BOX`` so that we know how many handles are around at
any time. To control the process, it is necessary to call a special
function, ``pixClone()`` or ``boxClone()`` to get a new handle (you
can't simply assign a new handle to the image!). It is also necessary to
call a destruction function (e.g., ``pixDestroy()``) on every handle.
Only when the final handle to a ``PIX`` or ``BOX`` is destroyed does the
reference count go to zero and the actual ``PIX`` or ``BOX`` structure
can be freed. By following these simple rules, the programmer can write
safe code without memory leaks, and without worrying about what handle
"owns" what structure.

A common programming pattern that uses the ``pixClone()`` arises when
you have an image processing function that specifies both a source and
destination image, where if the two images are the same, the operation
is intended to be in-place, but otherwise it is not. Most operations
cannot easily be done in-place, so the in-place situation is implemented
by first copying the source image to a temporary image, which then acts
as the source so that the result can be written to the input source
image. To simplify the use of both options in the implementation, if the
operation is not in-place, you still make a temporary image, but this
one is a clone of the source, so that it is really just another handle
to the same data structure. Then the operation always proceeds using the
temporary image as the source and writing the result into the
destination. Finally, the temporary image is always destroyed. If the
temporary image is a clone of the source, it will have a reference count
of 2, and its "destruction" will simply lower that count back to 1.

I mentioned above that we use reference counting to allow two "clients"
to hold on to the same data structure. The most important context in
which this applies is where the "clients" are pointer arrays; here, the
``PIXA`` and ``BOXA``. With reference counting, two ``PIXA`` arrays can
hold pointers to the same ``PIX``, and each can "own" it in the sense
that when the ``pixaDestroy()`` function is called on the two ``PIXA``,
no ``PIX`` is freed twice.

Here is a simple but very important rule that applies to all ptr arrays
that are not stacks or queues. It is often the case that you need to add
structures to the end of an array, but don't need to *replace* them. You
just accumulate them in the array, for use either individually or by
functions that use the whole array. For such arrays, of which the
``PIXA`` and ``BOXA`` are examples, it is simplest to provide two
functions: a procedure to add a structure to the end of the array and
another to access a structure within an array *without removing
it*. (Again, if you find you need to both add and remove structures from
the end of an array, you should use a stack or a queue.) Here's the rule
for accessing a structure without removing it:

   When you access something within an array using a "get" accessor, you
   have the choice of receiving a handle to the original structure (this
   is a *clone*, where the internal reference count has been incremented
   by 1) or a new copy of the original structure. You must use an
   accessor function; you are not allowed to simply get another pointer
   to the same structure without increasing the reference
   count. Further, you must dispatch the arrays with the array
   destruction function, which decrements the reference count of each
   element in the array and destroys those elements whose reference
   count goes to 0. You must also dispatch any element you retrieve from
   an array, either by explicitly destroying it with its destroy
   function, or by adding it to another array, allowing it to be
   destroyed at a later time. Consequently, when you access a structure
   within an array you have two obligations:

   #. Not to destroy the original structure.

   #. To destroy any copies or clones of that structure that you make.

It all comes down to *ownership*: the entity that is responsible for
destroying the object. To set up the safest programming environment
within the limitations of C, we do not allow access to a structure in an
array (of ``PIX`` or ``BOX``) without requiring a clone or copy to be
made, even if you only want to determine the value of some internal
field.  This still incurs a slight overhead with a clone, because you
must remember to destroy it.

Cloning with reference counting works well with arrays, but not for
lists that are implemented by embedding the list pointers within the
individual structures. Imagine what would happen if you tried to place
two clones of a structure in two different lists, using embedded list
pointers: when placing the clone in the second list you'd break the
first list, because there is really only one structure and hence only
one set of embedded list pointers. Consequently, when putting
reference-counted structures in lists, you must hang the structures
from separately allocated list cells that contain the list pointers
and maintain the list.


A low-level gotcha: operator precedence in C
============================================

If you plan to do any work with bit-level operators, you will run into
an operator precedence decision that Dennis Ritchie has admitted was the
worst in his design of C. It is interesting to note that the designers
of Java were willing to deviate from C by using only signed data and
introducing the ">>>" operator for right shift without sign propagation,
but they decided to keep the flawed C operator precedence intact for
compatibility.

The problem is in the precedence of the *bit logical operators*.
"Logically" these should have precedence comparable to bit arithmetic,
because that is what they really are. However, Ritchie dropped the
precedence down below the *relational operators* to just above the
*logical operators*.

This causes problems that are very difficult to find. For example,
suppose you want to test if a masked part of a word x is zero. If you
were to write:

.. sourcecode:: c

   if (x & mask == 0) { ... }

you would get the wrong result; namely, 

.. sourcecode:: c

   if (x & (mask == 0)) { ... }

because the relational "==" has higher precedence than the logical
bit-and. The test will always fail (assuming the mask is nonzero)
because it is doing a bit-and between x and 0; consequently, the block
will never execute. If this were somewhere within a large procedure
containing many bit logical and bit arithmetic operations, you are
almost guaranteed to have a miserable time trying to find the problem. A
good rule is: If in doubt, *add parentheses*. The safest rule is: *Just
add the damn parentheses*.


Anecdotes on managing complexity in programming
===============================================

.. epigraph::

   | *Mathematicians stand on each other's shoulders,*
   | *While computer scientists stand on each other's toes,*
   | *And computer engineers dig each other's graves.*

If you are going to write large programs, you must handle the complexity
that comes from interactions between different parts, and, in
particular, the pervasive influence of the "interfaces," both through
functions and data structures. I hope you find the following at least
entertaining.


Fred Hoyle's N\ :sup:`2` law of complexity
------------------------------------------

At age 16, I read Fred (later, Sir Fred) Hoyle's *Frontiers of
Astronomy*, which reinforced my belief that science was the highest
calling. Hoyle described the evolution of stars, and the nuclear
reactions that were going on inside, in a way that demonstrated the
power of observation and deductive logic.

Hoyle was an unusual person. He made fundamental contributions to our
understanding of nucleosynthesis in stars, and he worked on many
different things. He speculated on the archaeological dating and purpose
of Stonehenge. He gave lectures propounding a theory that flu viruses
come from outer space, his evidence being that pandemics supposedly
coincide with the 11 year solar activity cycle, and the flu spreads too
quickly to be passed from one person to another!

But this isn't the only instance where his speculations have been
soundly rejected by the scientific community. Hoyle formulated a
cosmological theory of the universe, called the *Steady State universe*,
and defended it for 50 years until he died, in spite of overwhelming
evidence to the contrary. Hoyle deprecatingly called Gamow's competing
idea the "Big Bang" theory, a name that stuck! The Big Bang has since
been confirmed by all experimental observations, and in particular, the
*cosmic microwave background* radiation at 3 degrees K. Hoyle's Steady
State cosmology was attractive in that it "solved" the problem of the
origin of the universe by removing it: he claimed that there was no
origin --- the universe has always been here, just as it is today. For
the density to remain constant in an expanding universe, matter must be
created out of the vacuum. Unfortunately for Hoyle, this has not been
observed at the required rate (or at any rate, for that matter). I find
it fascinating that Hoyle, along with his colleagues Gold, Narlikar and
Bondi, all brilliant scientists, stuck to their theory with a
stubbornness that defied logic. Why do these young people get an *ideé
fixé*, that forms the central core of their scientific career?

But I digress. Hoyle also enjoyed writing science fiction, and I eagerly
read each book as it came out. *A for Andromeda* appeared in 1962. The
plot has some young SETI (Search for Extra-Terrestrial Intelligence)
scientists discover an unusual signal from outer space. When they
finally crack the code -- I believe the "Rosetta Stone" for the code was
the frequency of some spectroscopic absorption line in hydrogen --- they
found that it was the description of a computer along with a mysterious
computer program. They built the machine, ran the program, and --- voilà
--- it made a human-like robot, Andromeda. Hoyle made one claim that
impressed me: *the complexity of a computer program goes as the square
of its size*. The program for Andromeda was huge, and its complexity was
consequently unimaginable.  Although I accepted Hoyle's claim, which was
based on some loose reasoning about how the parts interact, it left me
uneasy, because it stated that programming doesn't scale: *large programs
are not practical*.

Although Hoyle was wrong, I ran into a situation that seemed to support
his "law" soon after I went to Xerox. One of my colleagues gave me a
plotting program written in Fortran that needed to be modified. This
program was only about 500 lines long, but it was a maze of spaghetti
code, with 'goto' branches swarming throughout a single function. In
fact, the complexity may have been even higher than second power in
size! Here, the complexity came from the strange internal states and
twisted control flow, rather than from interfaces between different
parts.

Although I've been sympathetic ever since to people like Wirth who wish
to outlaw the 'goto' statement, I'm glad K&R included it in C because
'break' only takes you out one level.


Complexity at the interface
---------------------------

The center manager at Xerox PARC during the late 80s and 90s was a
character. He shall remain nameless; I'll only refer to him by the
initials of my sister Judith before she was married: jsb. I found it
interesting to listen to jsb when he was in freestyle pontification
mode. He would say strange things that were surely designed to rearrange
your neural connections. Most of what jsb said was nonsense, but if you
didn't take it seriously (and didn't tell him that you thought it was
nonsense), you were likely to survive the experience.

Over the years, jsb decided that "interfaces" were the key. The physics
lab at PARC had redirected its work in the mid-80s to "surface and
interface physics," but that's not what jsb had in mind. He was thinking
of interfaces between different disciplines, such as the complexity
studies at the Santa Fe Research Institute, and of programmatic
interfaces. jsb was sure that everything interesting happened at these
interfaces. Alan Perlis, a well-known computer scientist and author of
:unconverted:`120 programming epigrams
<cachedpages/perlis-epigrams.html>`, was a frequent visitor to PARC, and
he gave several lectures on how difficult it is to change program
interfaces. jsb decided the main problem of programming was this
complexity of the interfaces. He also continually urged people to go to
the root of the problem and come up with formal theories, rather than
ad-hoc solutions.

I decided to play an irreverent joke in 1993. At this time, each
laboratory manager collected and forwarded monthly a set of research
highlights up to the center manager, who would then send a subset on
to the Xerox VP of research. I wrote a research highlight, with the
winking approval of my laboratory manager, claiming that I had made a
radical architectural breakthrough and had solved the interface
problem in programming. My brilliant solution involved a large data
structure I called a "KitchenSink." All functions took a KitchenSink
and at most one other argument, and returned nothing of significance
(except for the one function that actually made a KitchenSink, of
course). In this bold stroke, I claimed to eliminate all of Perlis's
problems with interfaces. All "side-effects" went into the
KitchenSink, which itself was composed of an array of indeterminate
size of pointers ('void*' pointers for C), any of which could point to
an array or list of things. Among the things pointed to were, of
course, KitchenSinks, that had been configured into some application-
dependent formats, all eventually ending up as intrinsic types
supported by the specific language. I mentioned that the recursive use
of KitchenSinks was theoretically required to generate the complexity
of a Turning Machine. This was complete nonsense, just smoke and
mirrors to dress up the claim, but it fit with the AI paradigm of
using recursion because of its elegance. This was also in the era when
C++ and object-oriented programming were becoming fashionable, and I
emphasized the maximal use of data hiding in the KitchenSink.

jsb did not forward my "breakthrough" to the corporate level. I
believe that he was so astounded that an ex-physicist rather than an
AI person might solve the biggest problem (he thought) in computer
architecture, that he consulted my laboratory manager, who let him in
on the joke.

I had another chance to spoof jsb on his interface beliefs. I prepared a
humorous summary of conclusions from a mid-90s committee set up to
evaluate technological opportunities in computing. There, I used the
mathematics of high dimensional spaces, where the volume of a
hypersphere is nearly all within a very small distance from the surface,
to assert a proof that the interface is everything. The analogy and the
proof were silly --- I gave it to amuse the physicists.  But the
geometry is significant, because it links the statistical definition of
entropy (as proportional to the log of the number of accessible states)
to the thermodynamic definition. Consider two identical systems, one
completely isolated with known energy E and the second in contact with a
heat bath at some temperature, freely exchanging energy, and
consequently with an energy that averages to be E but has some
uncertainty. All thermodynamic properties of the two systems are
identical, so their entropies must be the same. But one has a fixed
energy E so that the accessible states occupy a very thin hypersphere
shell in momentum space, and the other occupies states in a thicker
shell. The conclusion is that the thickness of the shell thus doesn't
matter: the thinnest possible shell contains essentially all the states
in 10\ :sup:`23` dimensions!


Getting managed by complexity
-----------------------------

Another horror story with which I was slightly familiar was the
Textbridge OCR software developed first at Kurzweil and then at Xerox
Imaging Systems after Xerox acquired part of Kurzweil. The software had
been developed over a period of about 15 years. Initially, it performed
single font character recognition on an embedded machine with very
limited memory. Then crude page segmentation was added. Then the OCR was
improved to handle multiple fonts. Then the page segmentation was
further improved. Each step in development added to what was there
before, like the Winchester House in San Jose. The initial architectural
decision to express the image as a run-length data structure and throw
away the raster version, which made sense in the 1980s because RAM was
so expensive, conflicted with the need for accurate page
segmentation. As the system grew, it became ever more difficult to
change the architecture, and attempts to improve the OCR often had
complex and unintended side-effects, requiring massive regression
testing. After one version was shipped, there was never enough time to
change the interfaces for the next version. The original developers
left, along with some of the understanding of how things worked.

The software engineers who built, maintained and extended the system
were outstanding. They understood pattern classification and image
analysis, and were very careful. Yet ultimately, they were overwhelmed
by complexity. Perhaps some of them will eventually describe what they
learned about complexity and how to avoid it.


Managing the complexity
-----------------------

The holy grail is for complexity to scale linearly with program size.  I
believe this is achievable (or nearly so) using the object paradigm in
|Leptonica|.

Perlis's ninth epigram is as follows:

   It is better to have 100 functions operate on one data structure
   than 10 functions on 10 data structures.

One way to view this is to consider functions as verbs and data
structures as nouns. If you have many nouns, you must worry about the
results when they are acted on by each of the verbs, and you must insure
that the resulting side-effects are consistent for all these
cases. Hidden interdependencies make it difficult to maintain such
systems. In |Leptonica|, I have attempted to use as few nouns as
possible. The most important noun (the ``Pix``) is as simple as possible
so that it can easily be replaced by an equivalent noun that is used in
another application.

Although silly, the KitchenSink joke demonstrates that architectural
complexity is shared between function interfaces (verbs) and data
structures (nouns). There must be some balance: you don't want to use a
KitchenSink, but you need some data structures to bring order into the
application. Without data structures, all the data that needs to be in
scope must be passed in to a function or created there. For big
applications, this would be a nightmare, with long strings of arguments
of data passed between functions.

By contrast with this extreme, the object viewpoint is to have each
function be responsible for a task, to divide tasks up into subtasks
where appropriate, and to make a special data structure (one, if
possible) for an application, such as ``JbClasser`` in the jbig2
classifier. This structure keeps all state and contains (most of) the
data required for computation on it. You create the structure, you store
computation results in it, and you use it to generate whatever output is
required (such as images, or bounding boxes, or compressed file data,
etc.). And finally, you destroy it with one command. Above all, at the
application level you do not need to ask questions about what is
inside. The object manages the details that the application programmer
doesn't want to know about, and would be likely to cause problems if he
were forced to manage them.

When using a language like C, it is especially important to have a set
of classes (or structures) for common data sets, and for these to be
implemented with accessors and other safety factors (such as cloning
handles) so that the application programmer is unlikely to make a
mistake that will either crash the program or leak memory.

By subdividing programs up into simple, logical parts, and using a
library of (relatively) memory-safe functions on commonly-used data
structures, large applications can be built where it is clear what is
happening at each step. That, however, is not enough to manage
complexity. Consider two types of programs:

#. *Well determined*. The relation between the input data and the output
   data is specified to a level that allows unambiguous determination of
   correctness. Typically either or both the input and output are
   constrained to a high level. An example is 'ripping' a PostScript
   file into a raster for a specified output device.

#. *Badly determined*. The input data is often very weakly constrained,
   so that it is difficult both to anticipate how to handle it and to
   determine if the program is correct. An example is performing OCR on
   a badly degraded raster image of text.

Note that the process of going from a valid PostScript text file to a
raster is well determined, but the inverse process (image analysis) is
badly determined. It is in this second case, where the input is so
weakly constrained, that the biggest problems are faced in managing
complexity. Decisions have to be made based on characteristics of
arbitrary binary data, rather than using well-formed strings to run a
finite state machine that can be verified to behave correctly. This is
the frontier, where engineering faces its biggest challenges and
engineering principles have yet to be properly expressed.

Stepping into this frontier, I offer a few vague design principles for
building and tuning image analysis programs. This little section is a
work in progress, and I offer it with some humility. As mentioned
above, the difficulty in analyzing images is due to the fact that, to
a large extent, images are unstructured data. Unusual and unexpected
things can and do appear. Consequently,


#. *Avoid as much as possible making implicit assumptions about image
   content*. Implicit assumptions will get you every once in a while, or
   more often.

#. *Try to make all assumptions explicit, and as weak as possible*. A
   program that makes a bad assumption about image content is likely to
   fail. For example, if you're using connected components on binary
   images, don't assume that small components do not touch. If you're
   using topological methods, don't assume that large connected borders
   do not exist.

#. *Make decisions based on the most robust statistical basis possible*.
   Image analysis requires the nonlinear process of making decisions, but
   always try to do it on sufficient evidence.

#. *Avoid special casing. Of course, there are different basic
   situations, such as analyzing color, grayscale and binary
   images*. But if you're doing one of these, try to avoid bifurcations
   where you go off on some branch and don't return. If your processing
   is a tree with many branches, it is almost guaranteed to make serious
   mistakes, and to be difficult to tune.

#. *Try to organize the processing as a pipeline, along which things are
   analyzed and changed*. This is related to avoidance of special
   casing. Some images will not need some processing steps. Instead of
   using gotos, use a small set of integer and boolean parameters to
   select which processing stages an image is subject to. So if
   possible, let all the images follow the same "pipeline," but have
   some require more stuff to be done along the way.

#. *Don't take the pipeline analogy too far*. For example, don't
   actually try to build it with small executables that pipe data
   through. This architecture is often useful for image *processing*,
   but it is not appropriate for image *analysis*, where decisions must
   be made, steps must be conditionally skipped, loops must be used to
   handle different parts of the image independently, and parameters
   must be passed in to each stage.

#. *Use functions to perform specific tasks*. For each task, try to make
   a stable interface that has the fewest number of arguments necessary
   to handle the cases that will be presented. But see the next item!

#. *Do not bundle important parameters up in a class or data structure
   simply in order to hide them or to simplify the appearance of
   function interfaces*. It can be undesirable to hide the salient
   parameters. If a function uses certain arguments (e.g., images,
   masks, thresholds, etc.), I prefer to have them explicitly in the
   call, because it's easier to see exactly what is happening, to find
   mistakes, and to figure out how and where to tune things.

..
   Local Variables:
   coding: utf-8
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 72
   mode: auto-fill
   standard-indent: 3
   tab-stop-list: (3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60)
   End:
