DEFAULT_CODES = {
"B-001": "#include <stdio.h>\nint main(){\nint a;\nint b;\nscanf(\"%d %d\",&a,&b);\nint c;\nc=a+b;\nprintf(\"%d\",c);\nreturn 0;\n}",

"B-002": "#include <stdio.h>\nint main(){\nint a,b;\nscanf(\"%d %d\",&a,&b);\nif(a>b)\nprintf(\"%d\",a);\nelse\nprintf(\"%d\",b);\nreturn 0;\n}",

"B-003": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nif(n%2==0)\nprintf(\"Even\");\nelse\nprintf(\"Odd\");\nreturn 0;\n}",

"B-004": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint i,s=0;\nfor(i=1;i<=n;i++)\ns=s+i;\nprintf(\"%d\",s);\nreturn 0;\n}",

"B-005": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint i,f=1;\nfor(i=1;i<=n;i++)\nf=f*i;\nprintf(\"%d\",f);\nreturn 0;\n}",

"B-006": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint i;\nfor(i=1;i<=n;i++)\nprintf(\"%d \",i);\nprintf(\"\\n\");\nreturn 0;\n}",

"B-007": "#include <stdio.h>\nint main(){\nint a,b;\nscanf(\"%d %d\",&a,&b);\nint t=a;\na=b;\nb=t;\nprintf(\"%d %d\",a,b);\nreturn 0;\n}",

"B-008": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nif(n>0)\nprintf(\"Positive\");\nelse\nprintf(\"NotPositive\");\nreturn 0;\n}",

"B-009": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint s,c;\ns=n*n;\nc=s;\nprintf(\"%d\",c);\nreturn 0;\n}",

"B-010": "#include <stdio.h>\nint main(){\nchar c;\nscanf(\" %c\",&c);\nchar n;\nn=c+1;\nprintf(\"%c\",n);\nreturn 0;\n}",

"B-011": "#include <stdio.h>\nint main(){\nint x;\nscanf(\"%d\",&x);\nint y;\ny=x-1;\nx=y;\nprintf(\"%d\",x);\nreturn 0;\n}",

"B-012": "#include <stdio.h>\nint main(){\nint a;\nscanf(\"%d\",&a);\nint r;\nr=a%10;\na=r;\nprintf(\"%d\",a);\nreturn 0;\n}",

"B-013": "#include <stdio.h>\nint main(){\nint a,b;\nscanf(\"%d %d\",&a,&b);\nint r;\nr=a*b;\nb=r;\nprintf(\"%d\",b);\nreturn 0;\n}",

"B-014": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nif(n<0)\nn=-n;\nelse\nn=n;\nprintf(\"%d\",n);\nreturn 0;\n}",

"B-015": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint i,c=0;\nfor(i=1;i<=n;i++)\nc=c+1;\nprintf(\"%d\",c);\nreturn 0;\n}",

"B-016": "#include <stdio.h>\nint main(){\nint a;\nscanf(\"%d\",&a);\nint r;\nr=a*a;\na=r;\nprintf(\"%d\",a);\nreturn 0;\n}",

"B-017": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nif(n==0)\nprintf(\"Zero\");\nelse\nprintf(\"NonZero\");\nreturn 0;\n}",

"B-018": "#include <stdio.h>\nint main(){\nint n;\nscanf(\"%d\",&n);\nint i,s=1;\nfor(i=1;i<=n;i++)\ns=s+1;\nprintf(\"%d\",s);\nreturn 0;\n}",

"B-019": "#include <stdio.h>\nint main(){\nchar c;\nscanf(\" %c\",&c);\nchar d;\nd=c-1;\nc=d;\nprintf(\"%c\",c);\nreturn 0;\n}",

"B-020": "#include <stdio.h>\nint main(){\nint a,b;\nscanf(\"%d %d\",&a,&b);\nint r;\nr=a-b;\na=r;\nprintf(\"%d\",a);\nreturn 0;\n}"
}