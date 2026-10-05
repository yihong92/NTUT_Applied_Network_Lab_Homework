#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIDE 26
#define MAX_LINE 100

typedef struct {
    int i;
    int j;
    char level;
} Line;

char levels[5] = {'v', 'u', 't', 's', 'r'};
char lotID[MAX_SIDE];
int number[MAX_SIDE];
Line Horizontal_line_info[MAX_LINE];

int line_count = 0;
int sides;

/* 回傳 level 在 levels 中的索引 */
int levelIndex(char c) {
    for (int i = 0; i < 5; i++) {
        if (levels[i] == c)
            return i;
    }
    return -1;
}
void printHorizontal_line_info(Line info[], int count)
{
    printf("Horizontal_line_info:\n");

    for (int i = 0; i < count; i++) {
        printf("(%d, %d, %c)\n",
               info[i].i,
               info[i].j,
               info[i].level);
    }
}

int main() {

    printf("請輸入邊數\n>>> ");
    scanf("%d", &sides);

    for (int i = 0; i < sides; i++) {
        number[i] = i + 1;
        lotID[i] = 'A' + i;
    }

    getchar();

    printf("請輸入橫線資訊，其格式為 i,j,x! (輸入 q 結束)\n");

    while (1) {

        char input[50];

        printf(">>> ");
        /* ex: '1' ',' '2' ',' 't' '\n' '\0' */
        fgets(input, sizeof(input), stdin);
        /* fegets 字串包含 '/n' 需去除*/
        input[strcspn(input, "\n")] = '\0';

        if (strcmp(input, "q") == 0 || strcmp(input, "Q") == 0)
            break;

        int i, j;
        char x;

        if (sscanf(input, "%d,%d,%c", &i, &j, &x) != 3) {
            printf("格式錯誤!其格式為 i,j,x!\n");
            printf("目前共有 %d 條橫線\n", line_count);
            printHorizontal_line_info(Horizontal_line_info, line_count);
            continue;
        }

        if (levelIndex(x) == -1) {
            printf("格式錯誤!層只能輸入 v/u/t/s/r\n");
            printf("目前共有 %d 條橫線\n", line_count);
            printHorizontal_line_info(Horizontal_line_info, line_count);
            continue;
        }

        if (!(abs(i - j) == 1 || abs(i - j) == sides - 1)
            || i < 1 || i > sides
            || j < 1 || j > sides)
        {
            printf("格式錯誤!不是相鄰邊\n");
            printf("目前共有 %d 條橫線\n", line_count);
            printHorizontal_line_info(Horizontal_line_info, line_count);
            continue;
        }

        if (i > j) {
            int temp = i;
            i = j;
            j = temp;
        }

        int conflict = 0;

        for (int k = 0; k < line_count; k++) {

            if (Horizontal_line_info[k].level != x)
                continue;

            if (Horizontal_line_info[k].i == i ||
                Horizontal_line_info[k].i == j ||
                Horizontal_line_info[k].j == i ||
                Horizontal_line_info[k].j == j) {

                conflict = 1;
                break;
            }
        }

        if (conflict) {
            printf("格式錯誤! 重複橫線\n");
            printf("目前共有 %d 條橫線\n", line_count);
            printHorizontal_line_info(Horizontal_line_info, line_count);
            continue;
        }

        Horizontal_line_info[line_count].i = i;
        Horizontal_line_info[line_count].j = j;
        Horizontal_line_info[line_count].level = x;
        line_count++;

        printf("目前共有 %d 條橫線\n", line_count);
        printHorizontal_line_info(Horizontal_line_info, line_count);
    }

    /* swap[level][number] */
    int swap[5][MAX_SIDE + 1];

    memset(swap, 0, sizeof(swap));

    for (int k = 0; k < line_count; k++) {

        int idx = levelIndex(Horizontal_line_info[k].level);

        int a = Horizontal_line_info[k].i;
        int b = Horizontal_line_info[k].j;

        swap[idx][a] = b;
        swap[idx][b] = a;
    }

    printf("\n結果：\n");

    for (int person = 1; person <= sides; person++) {

        int cur = person;

        for (int lv = 0; lv < 5; lv++) {

            if (swap[lv][cur] != 0)
                cur = swap[lv][cur];
        }

        printf("No.%d 參賽者之籤碼為 [%c]\n",
               person,
               lotID[cur - 1]);
    }

    return 0;
}