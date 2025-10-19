#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

/*

The Romans have resurrected and are trying to take you for all you have! Reverse Engineer their Ransomware
to figure out how they encrypted your flag, and then decrypt it!

*/

int main()
{

    uint8_t key1 = 122;
    uint8_t key2 = 245;
    uint8_t key3 = 133;
    uint8_t key4 = 10;
    uint8_t key5 = 82;
    uint8_t key6 = 163;
    uint8_t key7 = 153;
    uint8_t key8 = 122;
    uint8_t key9 = 255;
    uint8_t key10 = 92;
    uint8_t key11 = 153;
    uint8_t key12 = 112;
    uint8_t key13 = 184;
    uint8_t key14 = 61;
    uint8_t key15 = 163;
    uint8_t key16 = 41;
    uint8_t key17 = 224;
    uint8_t key18 = 224;
    uint8_t key19 = 122;
    uint8_t key20 = 51;
    uint8_t key21 = 133;
    uint8_t key22 = 82;
    uint8_t key23 = 245;
    uint8_t key24 = 184;
    uint8_t key25 = 0;
    uint8_t key26 = 245;
    uint8_t key27 = 122;
    uint8_t key28 = 92;
    uint8_t key29 = 41;
    uint8_t key30 = 122;
    uint8_t key31 = 10;
    uint8_t key32 = 61;
    uint8_t key33 = 204;
    uint8_t key34 = 224;
    uint8_t key35 = 92;
    uint8_t key36 = 184;
    uint8_t key37 = 224;
    uint8_t key38 = 30;
    uint8_t key39 = 184;
    uint8_t key40 = 224;
    uint8_t key41 = 10;
    uint8_t key42 = 122;
    uint8_t key43 = 10;
    uint8_t key44 = 224;
    uint8_t key45 = 184;
    uint8_t key46 = 143;
    uint8_t key47 = 163;
    uint8_t key48 = 82;
    uint8_t key49 = 184;
    uint8_t key50 = 122;
    uint8_t key51 = 82;
    uint8_t key52 = 41;
    uint8_t key53 = 224;
    uint8_t key54 = 92;
    uint8_t key55 = 255;
    uint8_t key56 = 224;
    uint8_t key57 = 133;
    uint8_t key58 = 122;
    uint8_t key59 = 41;
    uint8_t key60 = 245;
    uint8_t key61 = 0;
    uint8_t key62 = 245;
    uint8_t key63 = 92;
    uint8_t key64 = 163;
    uint8_t key65 = 51;
    uint8_t key66 = 224;
    uint8_t key67 = 224;
    uint8_t key68 = 153;
    uint8_t key69 = 1;
    uint8_t key70 = 82;
    uint8_t key71 = 61;
    uint8_t key72 = 122;
    uint8_t key73 = 30;
    uint8_t key74 = 30;
    uint8_t key75 = 122;
    uint8_t key76 = 30;
    uint8_t key77 = 255;
    uint8_t key78 = 224;
    uint8_t key79 = 255;
    uint8_t key80 = 92;
    uint8_t key81 = 112;
    uint8_t key82 = 20;
    uint8_t key83 = 122;
    uint8_t key84 = 224;
    uint8_t key85 = 184;
    uint8_t key86 = 92;
    uint8_t key87 = 224;
    uint8_t key88 = 20;
    uint8_t key89 = 184;
    uint8_t key90 = 122;
    uint8_t key91 = 184;
    uint8_t key92 = 61;
    uint8_t key93 = 255;
    uint8_t key94 = 194;
    uint8_t key95 = 184;
    uint8_t key96 = 184;
    uint8_t key97 = 92;
    uint8_t key98 = 143;
    uint8_t key99 = 20;
    uint8_t key100 = 194;

    FILE *flagFile = fopen("flag.txt", "r+b");
    fseek(flagFile, 0, SEEK_END);
    long fileSize = ftell(flagFile);
    rewind(flagFile);

    // Read entire file into buffer
    unsigned char *buffer = malloc(fileSize);
    if (!buffer)
    {
        fprintf(stderr, "malloc failed\n");
        fclose(flagFile);
        return 1;
    }
    if (fread(buffer, 1, fileSize, flagFile) != (size_t)fileSize)
    {
        perror("fread");
        free(buffer);
        fclose(flagFile);
        return 1;
    }

    // Encrypt in-place by adding key10
    for (long i = 0; i < fileSize; i++)
    {
        buffer[i] = buffer[i] + key69;
    }

    fclose(flagFile);

    FILE* encryptThis = fopen("enc.txt", "w");
    
    if (fwrite(buffer, 1, fileSize, encryptThis) != (size_t)fileSize)
    {
        perror("fwrite");
        free(buffer);
        fclose(encryptThis);
        return 1;
    }

    // Clean up
    free(buffer);
    fclose(encryptThis);

    printf("\n\n\n\n\x1b[38;2;139;0;0m"
           "⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⠶⠾⠿⠛⠛⠻⠿⠶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⠀⢠⣾⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣄⠀⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⣿⠇⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡈⣿⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⣿⡆⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⣿⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⠸⣧⢸⡆⢀⣀⣀⣤⡀⠀⠀⢀⣤⣀⣀⡀⠀⡟⣸⡟⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⠀⠹⣿⠁⣿⣿⣿⣿⡟⠀⠀⠸⣿⣿⣿⣿⠆⣿⠟⠀⠀⠀⣀⠀⠀\n"
           "⠀⢰⡟⢿⣆⠀⠀⣿⠀⠙⢿⣿⠟⠀⣠⣄⠀⠹⣿⣿⠟⠀⢹⠀⠀⣠⡿⢻⣇⠀\n"
           "⣠⡾⠃⠈⠻⢷⣦⣽⣄⡀⠀⠀⠀⢸⣿⣿⣧⠀⠀⠀⢀⣠⣿⣤⡶⠟⠁⠘⢿⣆\n"
           "⠻⠷⠶⠶⣶⣤⣈⠙⠻⣿⣷⣦⠀⠸⠋⠙⠟⠀⣠⣾⣿⠟⠋⣁⣠⣴⠶⠶⠾⠟\n"
           "⠀⠀⠀⠀⠀⠉⠛⠿⣶⣼⠿⣿⣲⡤⡤⡤⢤⢰⣿⡏⣿⣶⠿⠛⠉⠀⠀⠀⠀⠀\n"
           "⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⡄⠻⣹⡟⡟⡟⣻⣻⠽⠁⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀\n"
           "⠀⠀⣶⠾⠶⠾⠟⠋⣁⣼⣷⡀⠀⠉⠉⠉⠉⠀⢀⣼⣧⣀⠉⠛⠷⠶⠿⣶⡄⠀\n"
           "⠀⠀⠙⣷⡄⢀⣴⠿⠛⠁⠀⠙⠳⠶⠤⠴⠶⠞⠋⠀⠈⠙⠻⣶⡄⠀⣾⠟⠁⠀\n"
           "⠀⠀⠀⢸⣷⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣶⡿⠀⠀⠀\n"
           "\x1b[0m\n\n\n\n");

    printf("/*************************************************************************************\\ \n\n");
    printf("  MWAHAAHAHAH SAY GOOD-BYTE TO YOUR FLAG EMPRESS PLACIDIA!!!!! >:) \n");
    printf("  OUR ENCRYPTION METHOD IS TOO STRONG TO BREAK. YOU HAVE TO PAY US >:D \n");
    printf("  PAY 18.BTC TO THE ADDRESS 1BEER4MINERSMAKEITRAINCOINSHUNT123 TO GET YOUR FLAG BACK,  \n");
    printf("  OR WE SACK ROME AND I TAKE HONORIA'S HAND IN MARRIAGE! SIGNED, ATTILA THE HUN.  \n\n");
    printf("/*************************************************************************************\\ \n\n");

    return 0;
}
