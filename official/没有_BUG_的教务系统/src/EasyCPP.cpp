// g++ -std=c++11 -Wl,-z,relro,-z,now -o EasyCPP_ EasyCPP.cpp

/* $ g++ --version
 * g++ (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609
 * Copyright (C) 2015 Free Software Foundation, Inc.
 * This is free software; see the source for copying conditions.  There is NO
 * warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */
#include<bits/stdc++.h>
#include<unistd.h>

using namespace std;

class Grade;

Grade *T;
char username[0x20];
char password[0xa0];
char temp_stu_num[0x78];

double calGrade(int score) {
    if (score < 60) return 0;
    if (score < 61) return 1;
    if (score < 64) return 1.3;
    if (score < 65) return 1.5;
    if (score < 68) return 1.7;
    if (score < 72) return 2;
    if (score < 75) return 2.3;
    if (score < 78) return 2.7;
    if (score < 82) return 3;
    if (score < 85) return 3.3;
    if (score < 90) return 3.7;
    if (score < 95) return 4;
    return 4.3;
}

class Grade {
    public:
        Grade():studentNum(NULL), calculusGrade(0), linearAlgebraGrade(0), 
                mechanicsGrade(0), cryptographyGrade(0) {
                    cout << "Initialization Success!" << endl;
                }

        Grade(string stu_num, int cal_grade, int lin_grade, int mac_grade, int cry_grade) {
            studentNum = new char[stu_num.length() + 1];
            strcpy(studentNum, stu_num.c_str());
            calculusGrade = cal_grade;
            linearAlgebraGrade = lin_grade;
            mechanicsGrade = mac_grade;
            cryptographyGrade = cry_grade;
            cout << "Initialization success!" << endl;
        }

        Grade(const Grade &g) {
            studentNum = new char[strlen(g.studentNum) + 1];
            strcpy(studentNum, g.studentNum);
            calculusGrade = g.calculusGrade;
            linearAlgebraGrade = g.linearAlgebraGrade;
            mechanicsGrade = g.mechanicsGrade;
            cryptographyGrade = g.cryptographyGrade;
        }

        Grade operator=(const Grade &g) {
            studentNum = new char[strlen(g.studentNum) + 1];
            strcpy(studentNum, g.studentNum);
            calculusGrade = g.calculusGrade;
            linearAlgebraGrade = g.linearAlgebraGrade;
            mechanicsGrade = g.mechanicsGrade;
            cryptographyGrade = g.cryptographyGrade;
        }

        void edit() {
            int read_num;
            cout << "Tell me the new STUDENT NUMBER(eg: PB19000001), please:" << endl;
            read_num = read(0, temp_stu_num, 0x77);
            temp_stu_num[0x77] = '\x00';
            if (read_num <= 0) return;
            studentNum = new char[read_num + 1];
            memcpy(studentNum, temp_stu_num, read_num);

            cout << "Now tell me his/her CALCULUS grade(0~100):" << endl;
            cin >> calculusGrade;
            if (calculusGrade < 0 || calculusGrade > 100) return;

            cout << "Then the LINEAR ALGEBRA grade:" << endl;
            cin >> linearAlgebraGrade;
            if (linearAlgebraGrade < 0 || linearAlgebraGrade > 100) return;

            cout << "MECHANICS grade:" << endl;
            cin >> mechanicsGrade;
            if (mechanicsGrade < 0 || mechanicsGrade > 100) return;

            cout << "The last one. CRYPTOGRAPHY grade:" << endl;
            cin >> cryptographyGrade;
            if (cryptographyGrade < 0 || cryptographyGrade > 100) return;

            cout << "STUDENT: " << studentNum << "GPA: " << fixed << setprecision(2)
                 << (calGrade(calculusGrade) * 6 + calGrade(linearAlgebraGrade) * 4 + calGrade(mechanicsGrade) * 4 + calGrade(cryptographyGrade) * 3.5)/(6 + 4 + 4 + 3.5)
                 << endl;
        }

        char* getStudentNum() {
            return studentNum;
        }

        ~Grade() {
            delete [] studentNum;
            studentNum = nullptr;
            calculusGrade = 0;
            linearAlgebraGrade = 0;
            mechanicsGrade = 0;
            cryptographyGrade = 0;
        }

    private:
        char* studentNum;
        int calculusGrade;
        int linearAlgebraGrade;
        int mechanicsGrade;
        int cryptographyGrade;
};

void setPassword() {
    char temp_password[0xa0];
    int count;
    memset(temp_password, '\x00', 0xa0);
    cout << "You are admin, so you can set your password as you want!" << endl;
    cout << "Your new password: " << endl;
    count = read(0, temp_password, 0x9f);
    temp_password[count] = '\x00';
    memcpy(password, temp_password, count + 1);
}

void editInfo() {
    Grade origin_grade;
    origin_grade = *T;
    cout <<"STUDENT: " << origin_grade.getStudentNum() << endl;
    T->edit();
}

int main(int argc, char *argv[]) {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    char temp_username[0x20];
    char temp_password[0xa0];
    int i, count, choice;
    string stu_num = "PB19000001";

    cout << "Welcome to Academic Teaching Affair Management System!" << endl;
    cout << "You should LOGIN as ADMIN to use this system!" << endl;
    cout << "Username:";
    cin.getline(temp_username, 0x20);
    strncpy(username, temp_username, 0x1f);
    if(strncmp(temp_username, "admin", 5)) {
        cout << "Bad guy! You are not ADMIN!" << endl;
        exit(0);
    }

    cout << "Password:";
    count = read(0, temp_password, 0x9f);
    temp_password[count] = '\x00';
    memcpy(password, temp_password, count + 1);

    for (i = 0; i <= 7; ++i)
        temp_password[i] = ((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) | i) & ~((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) & i);
    if(memcmp(temp_password, "\x44\x00\x02\x41\x43\x47\x10\x63\x00", 9)) {
        cout << "Bad guy! Wrong password!" << endl;
        exit(0);
    }



    T = new Grade(stu_num, 100, 100, 100, 100);

    cout << "Welcome! Admin! I've missed you so much!" << endl;
    cout << "You could do two things, my matser:" << endl;
    cout << "1. edit student infomation" << endl;
    cout << "2. change your password" << endl;
    cout << "For the security of the system, I suggest you change your password everytime before editing!" << endl;


    while(1) {
        cout << "Please tell me your choice:";
        cin >> choice;
        getchar();
        switch(choice) {
            case 1:
                setPassword();
                editInfo();
                break;
            case 2:
                setPassword();
                break;
        }
    }
}


