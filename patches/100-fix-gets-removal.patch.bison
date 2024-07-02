--- a/lib/stdio.in.h
+++ b/lib/stdio.in.h
@@ -177,12 +177,6 @@ _GL_WARN_ON_USE (fflush, "fflush is not 
                  "use gnulib module fflush for portable POSIX compliance");
 #endif
 
-/* It is very rare that the developer ever has full control of stdin,
-   so any use of gets warrants an unconditional warning.  Assume it is
-   always declared, since it is required by C89.  */
-#undef gets
-_GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
-
 #if @GNULIB_FOPEN@
 # if @REPLACE_FOPEN@
 #  if !(defined __cplusplus && defined GNULIB_NAMESPACE)
