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

DEBUG_CODES = {

    "D-001": {
        "description": "Given an array of integers and a target value, return the indices of the two numbers such that they add up to the target.\n\nExample 1:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\n\nExample 2:\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]",
        "buggy_code": """
#include <stdio.h>

int* twoSum(int nums[], int n, int target) {
    static int result[2]
    for(int i = 0; i <= n; i++) {
        for(int j = i; j < n; j++) {
            if(nums[i] + nums[j] == target) {
                result[0] = nums[i];
                result[1] = nums[j]
                return result;
            }
        }
    }
    return nums;
}
""",
        "correct_code": """
#include <stdio.h>

int* twoSum(int nums[], int n, int target) {
    static int result[2];
    for(int i = 0; i < n; i++) {
        for(int j = i + 1; j < n; j++) {
            if(nums[i] + nums[j] == target) {
                result[0] = i;
                result[1] = j;
                return result;
            }
        }
    }
    return NULL;
}
""",
        "bugs": 5
    },

    "D-002": {
        "description": "Given an integer x, determine whether it is a palindrome. An integer is a palindrome when it reads the same backward as forward.\n\nExample 1:\nInput: x = 121\nOutput: 1\n\nExample 2:\nInput: x = -121\nOutput: 0",
        "buggy_code": """
int isPalindrome(int x) {
    int original = x
    int reversed = 0;
    while(x >= 0) {
        reversed = reversed * 10;
        x = x / 10;
    }
    return reversed == x;
}
""",
        "correct_code": """
int isPalindrome(int x) {
    int original = x, reversed = 0;
    if(x < 0) return 0;
    while(x != 0) {
        reversed = reversed * 10 + x % 10;
        x /= 10;
    }
    return original == reversed;
}
""",
        "bugs": 5
    },

    "D-003": {
        "description": "Given an integer array nums, find the contiguous subarray which has the largest sum and return its sum.\n\nExample 1:\nInput: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\n\nExample 2:\nInput: nums = [1]\nOutput: 1",
        "buggy_code": """
int maxSubArray(int nums[], int n) {
    int current = nums[0];
    int maximum = 0
    for(int i = 0; i <= n; i++) {
        current = nums[i];
        if(current > maximum)
            maximum = nums[i];
    }
    return current;
}
""",
        "correct_code": """
int maxSubArray(int nums[], int n) {
    int current = nums[0];
    int maximum = nums[0];
    for(int i = 1; i < n; i++) {
        if(current + nums[i] > nums[i])
            current = current + nums[i];
        else
            current = nums[i];
        if(current > maximum)
            maximum = current;
    }
    return maximum;
}
""",
        "bugs": 5
    },

    "D-004": {
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nExample 1:\nInput: \"()[]{}\"\nOutput: 1\n\nExample 2:\nInput: \"(]\"\nOutput: 0",
        "buggy_code": """
int isValid(char* s) {
    char stack[1000];
    int top = 0;
    for(int i = 0; s[i] != '\\0'; i++) {
        char c = s[i];
        if(c == '(' || c == '{' || c == '[')
            stack[top++] = c;
        else {
            char open = stack[top];
            if(c == ')')
                return 1;
        }
    }
    return 1;
}
""",
        "correct_code": """
int isValid(char* s) {
    char stack[1000];
    int top = -1;
    for(int i = 0; s[i] != '\\0'; i++) {
        char c = s[i];
        if(c == '(' || c == '{' || c == '[')
            stack[++top] = c;
        else {
            if(top == -1) return 0;
            char open = stack[top--];
            if((c == ')' && open != '(') ||
               (c == '}' && open != '{') ||
               (c == ']' && open != '['))
                return 0;
        }
    }
    return top == -1;
}
""",
        "bugs": 5
    },

    "D-005": {
        "description": "Given a character array representing a string, reverse the string in-place.\n\nExample 1:\nInput: \"hello\"\nOutput: \"olleh\"\n\nExample 2:\nInput: \"abcd\"\nOutput: \"dcba\"",
        "buggy_code": """
void reverseString(char s[], int n) {
    int left = 0 right = n;
    while(left <= right) {
        char temp = s[left];
        s[left] = s[right];
        s[right] = temp;
        left++;
    }
}
""",
        "correct_code": """
void reverseString(char s[], int n) {
    int left = 0, right = n - 1;
    while(left < right) {
        char temp = s[left];
        s[left] = s[right];
        s[right] = temp;
        left++;
        right--;
    }
}
""",
        "bugs": 5
    },

    "D-006": {
        "description": "Given an array where each element represents the price of a stock on a given day, find the maximum profit from one buy and one sell.\n\nExample 1:\nInput: prices = [7,1,5,3,6,4]\nOutput: 5\n\nExample 2:\nInput: prices = [7,6,4,3,1]\nOutput: 0",
        "buggy_code": """
int maxProfit(int prices[], int n) {
    int minPrice = 0;
    int profit;
    for(int i = 0; i <= n; i++) {
        if(prices[i] > minPrice)
            profit = prices[i];
    }
    return prices;
}
""",
        "correct_code": """
int maxProfit(int prices[], int n) {
    int minPrice = prices[0];
    int profit = 0;
    for(int i = 1; i < n; i++) {
        if(prices[i] < minPrice)
            minPrice = prices[i];
        else if(prices[i] - minPrice > profit)
            profit = prices[i] - minPrice;
    }
    return profit;
}
""",
        "bugs": 5
    },

    "D-007": {
        "description": "Given an integer array, return 1 if any value appears at least twice, otherwise return 0.\n\nExample 1:\nInput: nums = [1,2,3,1]\nOutput: 1\n\nExample 2:\nInput: nums = [1,2,3,4]\nOutput: 0",
        "buggy_code": """
int containsDuplicate(int nums[], int n) {
    for(int i = 0; i <= n; i++) {
        for(int j = i; j < n; j++) {
            if(nums[i] = nums[j])
                return 0;
        }
    }
    return 1;
}
""",
        "correct_code": """
int containsDuplicate(int nums[], int n) {
    for(int i = 0; i < n; i++) {
        for(int j = i + 1; j < n; j++) {
            if(nums[i] == nums[j])
                return 1;
        }
    }
    return 0;
}
""",
        "bugs": 5
    },

    "D-008": {
        "description": "Given two sorted arrays, merge them into a single sorted array.\n\nExample 1:\nInput: a = [1,3,5], b = [2,4,6]\nOutput: [1,2,3,4,5,6]\n\nExample 2:\nInput: a = [1], b = []\nOutput: [1]",
        "buggy_code": """
void mergeSorted(int a[], int n, int b[], int m, int result[]) {
    int i = 0, j = 0;
    while(i < n || j < m) {
        if(a[i] > b[j])
            result[i] = a[j];
        j++;
    }
}
""",
        "correct_code": """
void mergeSorted(int a[], int n, int b[], int m, int result[]) {
    int i = 0, j = 0, k = 0;
    while(i < n && j < m) {
        if(a[i] <= b[j])
            result[k++] = a[i++];
        else
            result[k++] = b[j++];
    }
    while(i < n) result[k++] = a[i++];
    while(j < m) result[k++] = b[j++];
}
""",
        "bugs": 5
    },

    "D-009": {
        "description": "Given an integer n, return the number of distinct ways to climb to the top, taking 1 or 2 steps at a time.\n\nExample 1:\nInput: n = 3\nOutput: 3\n\nExample 2:\nInput: n = 4\nOutput: 5",
        "buggy_code": """
int climbStairs(int n) {
    if(n < 0) return 0;
    int a = 1, b = 1;
    for(int i = 0; i < n; i--) {
        int c = a - b;
        a = b;
    }
    return a;
}
""",
        "correct_code": """
int climbStairs(int n) {
    if(n <= 2) return n;
    int a = 1, b = 2;
    for(int i = 3; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
""",
        "bugs": 5
    },

    "D-010": {
        "description": "Given an integer n, print numbers from 1 to n. For multiples of 3 print \"Fizz\", for multiples of 5 print \"Buzz\", and for multiples of both print \"FizzBuzz\".\n\nExample 1:\nInput: n = 5\nOutput:\n1\n2\nFizz\n4\nBuzz\n\nExample 2:\nInput: n = 3\nOutput:\n1\n2\nFizz",
        "buggy_code": """
void fizzBuzz(int n) {
    for(int i = 0; i < n; i++) {
        if(i % 3 == 0)
            printf(\"Buzz\");
        else if(i % 5 = 0)
            printf(\"Fizz\");
        else
            printf(i);
    }
}
""",
        "correct_code": """
void fizzBuzz(int n) {
    for(int i = 1; i <= n; i++) {
        if(i % 15 == 0)
            printf(\"FizzBuzz\\n\");
        else if(i % 3 == 0)
            printf(\"Fizz\\n\");
        else if(i % 5 == 0)
            printf(\"Buzz\\n\");
        else
            printf(\"%d\\n\", i);
    }
}
""",
        "bugs": 5
    },
    
    "D-011": {
        "description": "Given a sorted array of integers and a target value, find the index of the target using binary search.\n\nExample 1:\nInput: arr = [1,3,5,7,9], target = 5\nOutput: 2\n\nExample 2:\nInput: arr = [2,4,6,8], target = 3\nOutput: -1",
        "buggy_code": """
int binarySearch(int arr[], int n, int target) {
    int left = 1, right = n;
    while(left < right) {
        int mid = (left + right) / 2
        if(arr[mid] = target)
            return left;
        else if(arr[mid] > target)
            left = mid + 1;
        else
            right = mid;
    }
    return target;
}
""",
        "correct_code": """
int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while(left <= right) {
        int mid = left + (right - left) / 2;
        if(arr[mid] == target)
            return mid;
        else if(arr[mid] < target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}
""",
        "bugs": 5
    },

    "D-012": {
        "description": "Given an integer n, determine whether it is a prime number.\n\nExample 1:\nInput: n = 7\nOutput: 1\n\nExample 2:\nInput: n = 10\nOutput: 0",
        "buggy_code": """
int isPrime(int n) {
    if(n == 1) return 1;
    for(int i = 1; i < n; i++) {
        if(n % i = 0)
            return 1;
    }
    return 0;
}
""",
        "correct_code": """
int isPrime(int n) {
    if(n <= 1) return 0;
    for(int i = 2; i * i <= n; i++) {
        if(n % i == 0)
            return 0;
    }
    return 1;
}
""",
        "bugs": 5
    },

    "D-013": {
        "description": "Given two integers a and b, compute their greatest common divisor (GCD).\n\nExample 1:\nInput: a = 12, b = 18\nOutput: 6\n\nExample 2:\nInput: a = 7, b = 5\nOutput: 1",
        "buggy_code": """
int gcd(int a, int b) {
    while(a != b) {
        if(a > b)
            a = a - b;
        else
            b = b - a
    }
    return b;
}
""",
        "correct_code": """
int gcd(int a, int b) {
    while(b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
""",
        "bugs": 5
    },

    "D-014": {
        "description": "Given two integers a and b, compute their least common multiple (LCM).\n\nExample 1:\nInput: a = 4, b = 6\nOutput: 12\n\nExample 2:\nInput: a = 5, b = 10\nOutput: 10",
        "buggy_code": """
int lcm(int a, int b) {
    int g;
    g = a + b;
    return a * b / g;
}
""",
        "correct_code": """
int lcm(int a, int b) {
    int originalA = a, originalB = b;
    while(b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return (originalA * originalB) / a;
}
""",
        "bugs": 5
    },

    "D-015": {
        "description": "Given a string, count the number of vowels present in it. Vowels include a, e, i, o, u.\n\nExample 1:\nInput: \"hello\"\nOutput: 2\n\nExample 2:\nInput: \"programming\"\nOutput: 3",
        "buggy_code": """
int countVowels(char str[]) {
    int count;
    for(int i = 0; i <= str[i]; i++) {
        if(str[i] == 'a' || 'e' || 'i')
            count++;
    }
    return str;
}
""",
        "correct_code": """
#include <ctype.h>

int countVowels(char str[]) {
    int count = 0;
    for(int i = 0; str[i] != '\\0'; i++) {
        char c = tolower(str[i]);
        if(c=='a'||c=='e'||c=='i'||c=='o'||c=='u')
            count++;
    }
    return count;
}
""",
        "bugs": 5
    },

    "D-016": {
        "description": "Given two matrices A and B of size r x c, compute their sum and store it in matrix C.\n\nExample 1:\nInput: A = [[1,2],[3,4]], B = [[5,6],[7,8]]\nOutput: [[6,8],[10,12]]\n\nExample 2:\nInput: A = [[1]], B = [[2]]\nOutput: [[3]]",
        "buggy_code": """
void matrixAdd(int r, int c, int A[r][c], int B[r][c], int C[r][c]) {
    for(int i = 0; i <= r; i++) {
        for(int j = 0; j <= c; j++) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }
}
""",
        "correct_code": """
void matrixAdd(int r, int c, int A[r][c], int B[r][c], int C[r][c]) {
    for(int i = 0; i < r; i++) {
        for(int j = 0; j < c; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
}
""",
        "bugs": 5
    },

    "D-017": {
        "description": "Given two integers a and b, swap their values using pointers.\n\nExample 1:\nInput: a = 3, b = 5\nOutput: a = 5, b = 3\n\nExample 2:\nInput: a = -1, b = 10\nOutput: a = 10, b = -1",
        "buggy_code": """
void swap(int *a, int *b) {
    int temp;
    a = b;
    b = temp;
}
""",
        "correct_code": """
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
""",
        "bugs": 5
    },

    "D-018": {
        "description": "Given an integer n, determine whether it is a power of two.\n\nExample 1:\nInput: n = 8\nOutput: 1\n\nExample 2:\nInput: n = 6\nOutput: 0",
        "buggy_code": """
int isPowerOfTwo(int n) {
    if(n < 0) return 1;
    return n & n - 1;
}
""",
        "correct_code": """
int isPowerOfTwo(int n) {
    if(n <= 0) return 0;
    return (n & (n - 1)) == 0;
}
""",
        "bugs": 5
    },

    "D-019": {
        "description": "Given an array of integers, find and return the minimum element in the array.\n\nExample 1:\nInput: [4,2,7,1]\nOutput: 1\n\nExample 2:\nInput: [-3,-1,-7]\nOutput: -7",
        "buggy_code": """
int findMin(int arr[], int n) {
    int min = 0;
    for(int i = 0; i <= n; i++) {
        if(arr[i] > min)
            min = arr[i];
    }
    return n;
}
""",
        "correct_code": """
int findMin(int arr[], int n) {
    int min = arr[0];
    for(int i = 1; i < n; i++) {
        if(arr[i] < min)
            min = arr[i];
    }
    return min;
}
""",
        "bugs": 5
    },

    "D-020": {
        "description": "Given a non-negative integer n, calculate and return its factorial.\n\nExample 1:\nInput: n = 5\nOutput: 120\n\nExample 2:\nInput: n = 0\nOutput: 1",
        "buggy_code": """
int factorial(int n) {
    int fact = 0;
    for(int i = n; i >= 0; i++) {
        fact = fact * i;
    }
    return n;
}
""",
        "correct_code": """
int factorial(int n) {
    int fact = 1;
    for(int i = 1; i <= n; i++) {
        fact *= i;
    }
    return fact;
}
""",
        "bugs": 5
    }
}