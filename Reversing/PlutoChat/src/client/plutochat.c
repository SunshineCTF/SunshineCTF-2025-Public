#include <stdint.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>


enum packet_type {
    LOGIN,
    LOGIN_SUCCESSFUL,
    MESSAGE_SEND,
    MESSAGE_RECV
};
struct arc4_context
{
    uint8_t i;
    uint8_t j;
    uint8_t s[256];
};
static inline void arc4_swap(struct arc4_context* ctx, size_t i, size_t j)
{
    uint8_t const t = ctx->s[i];
    ctx->s[i] = ctx->s[j];
    ctx->s[j] = t;
}

static inline uint8_t arc4_next(struct arc4_context* ctx)
{

    ctx->i += 1;
    ctx->j += ctx->s[ctx->i];

    arc4_swap(ctx, ctx->i, ctx->j);

    return ctx->s[(uint8_t)(ctx->s[ctx->i] + ctx->s[ctx->j])];
}

void arc4_init(struct arc4_context* ctx, void const* key, size_t key_length)
{
    ctx->i = 0;
    ctx->j = 0;

    for (size_t i = 0; i < 256; ++i)
    {
        ctx->s[i] = (uint8_t)i;
    }

    for (size_t i = 0, j = 0; i < 256; ++i)
    {
        j = (uint8_t)(j + ctx->s[i] + ((uint8_t const*)key)[i % key_length]);
        arc4_swap(ctx, i, j);
    }
}

void arc4_process(struct arc4_context* ctx, void* src_data, void* dst_data, size_t data_length)
{

    if (data_length == 0)
    {
        return;
    }

    for (size_t i = 0; i < data_length; ++i)
    {
        ((uint8_t*)dst_data)[i] = ((uint8_t const*)src_data)[i] ^ arc4_next(ctx);
    }
}

void arc4_discard(struct arc4_context* ctx, size_t length)
{
    for (size_t i = 0; i < length; ++i)
    {
        arc4_next(ctx);
    }
}

uint32_t rotl32(uint32_t var, uint32_t hops) {
    return (var << hops) | (var >> ((32 - hops) & 31));
}

// KDF

unsigned char index_rearrange[] = {
    13, 8, 17, 12, 14, 7, 0, 5, 9, 4, 11, 16, 6, 18, 10, 1, 2, 3, 15, 19
};

unsigned char index_reval[] = {
    0xba, 0x79, 0xce, 0x55, 0x64, 0x13, 0x62, 0x21, 0xbf, 0xcc, 0x96, 0x0f, 0x68, 0x95, 0x2d, 0x51, 
    0x7a, 0x59, 0xf6, 0x44, 0xe5, 0x43, 0x3e, 0xb3, 0xa3, 0x81, 0x4f, 0xa6, 0x36, 0xfb, 0x6d, 0xf8, 
    0xf7, 0x1f, 0x6b, 0x42, 0xa7, 0xb7, 0xbc, 0x71, 0x0d, 0xb4, 0xe0, 0xb9, 0x25, 0x0a, 0x28, 0xa1, 
    0x76, 0x86, 0x6c, 0x27, 0xd9, 0x2a, 0x6a, 0x03, 0xf1, 0x72, 0xdb, 0x54, 0x82, 0x6f, 0xbb, 0x1c, 
    0x5a, 0x38, 0xd2, 0xbe, 0x09, 0x9b, 0x15, 0xb8, 0x8f, 0x78, 0x4c, 0x34, 0x67, 0xd7, 0xab, 0x75, 
    0x45, 0x87, 0x9d, 0x10, 0xe8, 0xeb, 0x32, 0x8d, 0xc5, 0x46, 0x65, 0x0b, 0x35, 0xbd, 0xea, 0x06, 
    0xa5, 0xdd, 0xa4, 0x5f, 0x40, 0x5d, 0xfc, 0x9a, 0x5b, 0xcb, 0x89, 0x91, 0x5c, 0xfe, 0x66, 0xfd, 
    0xaa, 0x37, 0x02, 0x12, 0x98, 0x6e, 0x17, 0xc9, 0x50, 0x20, 0x39, 0xc2, 0xed, 0xe7, 0xb2, 0x74, 
    0xe2, 0xef, 0x16, 0x5e, 0x99, 0x47, 0xf5, 0x1e, 0x23, 0x01, 0x57, 0xa0, 0x3b, 0x1b, 0x2b, 0xee, 
    0xc1, 0x58, 0x9e, 0xa9, 0xca, 0xff, 0xc4, 0x7b, 0x4b, 0x8e, 0x48, 0xcd, 0x7c, 0xc0, 0x56, 0xd0, 
    0x33, 0xc7, 0x70, 0x8b, 0xe1, 0x8c, 0xc3, 0x0e, 0x1d, 0x3d, 0xda, 0xcf, 0x11, 0x73, 0xec, 0xc6, 
    0x92, 0xb6, 0x26, 0x05, 0xfa, 0xf0, 0xe6, 0x0c, 0x14, 0x69, 0x61, 0xc8, 0x60, 0x31, 0x9c, 0x22, 
    0xac, 0x9f, 0x4e, 0x49, 0x29, 0x3f, 0x85, 0xf3, 0x53, 0xf9, 0x63, 0xdf, 0xd3, 0xf2, 0x00, 0x2e, 
    0x18, 0xd1, 0xde, 0x8a, 0x52, 0x08, 0xe9, 0xa2, 0xe4, 0x3a, 0x83, 0x7f, 0x94, 0xb5, 0xd4, 0xd5,
    0x77, 0x07, 0xdc, 0x19, 0x84, 0xd8, 0xaf, 0xa8, 0x93, 0x7e, 0xd6, 0x2c, 0xf4, 0x41, 0xb1, 0x2f, 
    0x7d, 0x4d, 0x97, 0x1a, 0x3c, 0xb0, 0x80, 0x90, 0x4a, 0xae, 0x24, 0x88, 0xad, 0x04, 0x30, 0xe3
};
void ARC4_init_from_seed(struct arc4_context *ctx, int seed) {
    unsigned int *key = malloc(80);
    unsigned int tmp;
    unsigned char last_byte;
    unsigned char tmp2;
    unsigned char *S = malloc(256);
    for(int i=0; i<20; i++) {
        key[i] = seed;
        seed = rotl32(seed, seed & 0b1111);
    }
    for(int i=0; i<20; i++) {
        tmp = key[i];
        key[i] = key[index_rearrange[i]];
        key[index_rearrange[i]] = tmp;
    }
    for(int i=0; i<80; i++) {
        tmp2 = ((unsigned char *)key)[i];
        ((unsigned char *)key)[i] = index_reval[tmp2] ^ last_byte;
        last_byte = ((unsigned char *)key)[i]; 
    }
    arc4_init(ctx, (unsigned char *)key, 80);
}

uint32_t randnum() {
    return ((uint32_t)rand() << 16) | rand();
}

// packet sending
void send_packet(int sockfd, unsigned char* data, size_t length) {
    unsigned char *enc_data = malloc(length + 8);
    unsigned int seed = randnum();
    ((int *)enc_data)[0] = seed; // set seed
    ((int *)enc_data)[1] = length; // set seed
    // create context
    struct arc4_context *ctx = malloc(sizeof(struct arc4_context));
    ARC4_init_from_seed(ctx, seed);
    arc4_process(ctx, data, enc_data+8, length);
    send(sockfd, enc_data, length+8, 0);
}
void send_msg(int sockfd, char *username, char *msg) {
    unsigned char username_length = strlen(username); 
    if (username_length > 0 && username[username_length - 1] == '\n') {
        username[username_length - 1] = '\0';
        username_length--;
    }
    unsigned char msg_length = strlen(msg);
    if (msg_length > 0 && msg[msg_length - 1] == '\n') {
        msg[msg_length - 1] = '\0';
        msg_length--;
    }
    unsigned char *data = malloc(msg_length + username_length + 3);
    data[0] = MESSAGE_SEND;
    data[1] = username_length;
    memcpy(data+2, username, username_length);
    data[2+username_length] = msg_length;
    memcpy(data+3+username_length, msg, msg_length);
    send_packet(sockfd, data, msg_length + username_length + 3);
}
void send_login(int sockfd, char *username, char *password) {
    unsigned char username_length = strlen(username);
    if (username_length > 0 && username[username_length - 1] == '\n') {
        username[username_length - 1] = '\0';
        username_length--;
    }
    unsigned char password_length = strlen(password);
    if (password_length > 0 && password[password_length - 1] == '\n') {
        password[password_length - 1] = '\0';
        password_length--;
    }
    unsigned char *data = malloc(password_length + username_length + 3);
    data[0] = LOGIN;
    data[1] = username_length;
    memcpy(data+2, username, username_length);
    data[2+username_length] = password_length;
    memcpy(data+3+username_length, password, password_length);
    send_packet(sockfd, data, password_length + username_length + 3);
}



void chat_menu(int sockfd) {
    char recv_username[256];
    char msg[256];
    while(1) {
        printf("Type a username to send a message to, or 'EXIT' to exit: ");
        fgets(recv_username, 256, stdin);
        if(strcmp(recv_username, "EXIT") == 0) {
            printf("Exiting PlutoChat...\n");
            exit(0);
        }
        while(1) {
            printf("Send a message to %s (or 'EXIT' to select a new user): ", recv_username);
            fgets(msg, 256, stdin);
            if(strcmp(msg, "EXIT") == 0) {
                break;
            }
            send_msg(sockfd, recv_username, msg);
        }
    }
}
typedef struct {
    int socket_fd;
} chat_args_t;

int logged_in = 0;
void recv_packet(int sockfd) {
    srand(time(NULL));
    unsigned char packet[2048];
    unsigned int seed, length;
    unsigned char sent_from_length;
    enum packet_type type;
    read(sockfd, packet, 8);
    seed = ((int *)packet)[0];
    length = ((int *)packet)[1];
    struct arc4_context *ctx = malloc(sizeof(struct arc4_context));
    ARC4_init_from_seed(ctx, seed);
    read(sockfd, packet+8, length);
    arc4_process(ctx, packet+8, packet+8, length);  
    type = packet[8];
    switch(type) {
        case LOGIN_SUCCESSFUL:
            printf("Login successful! Welcome to PlutoChat!\n");
            logged_in = 1;
            break;
        case MESSAGE_RECV:
            sent_from_length = packet[9];
            char *sent_from = malloc(sent_from_length+1);
            for(int i=0; i<sent_from_length; i++) {
                sent_from[i] = packet[10+i];
            }
            unsigned char msg_length = packet[10+sent_from_length];
            char *msg = malloc(msg_length+1);
            for(int i=0; i<msg_length; i++) {
                msg[i] = packet[11+sent_from_length+i];
            }
            printf("%d %d\n", msg_length, sent_from_length);
            printf("New message from %s: %s\n", sent_from, msg);
            break;
    }
}



void *chat_thread(void *thread_arg) {
    chat_args_t *args = (chat_args_t *)thread_arg;
    int socket_fd = args->socket_fd;
    while(1) {
        recv_packet(socket_fd);
    }
    free(args); 
    return NULL;
}


int new_chat_thread(int socket_fd) {
    pthread_t thread_id;
    chat_args_t *args = (chat_args_t *)malloc(sizeof(chat_args_t));
     if (args == NULL) {
        perror("There was an error initializing PlutoChat. Please try again.");
        return -1;
    }
    args->socket_fd = socket_fd;

    int ret = pthread_create(&thread_id, NULL, chat_thread, (void *)args);
    if (ret != 0) {
        perror("There was an error initializing PlutoChat. Please try again.");
        free(args);
        return -1;
    }
    pthread_detach(thread_id);
    return 0;
}

int main(int argc, char *argv[]) {
    char username[256];
    char password[256];
    int sockfd, connfd;
    struct sockaddr_in servaddr, cli;
    printf("Login to PlutoChat\n");
    printf("Username: ");
    fgets(username, 256, stdin);
    printf("Password: ");
    fgets(password, 256, stdin);
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Could not connect to PlutoChat servers. Try again later!\n");
        exit(0);
    }
    bzero(&servaddr, sizeof(servaddr));

    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(31337);

    // connect the client socket to server socket
    if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr))
        != 0) {
        printf("Could not connect to PlutoChat servers. Try again later!\n");
        exit(0);
    }

    new_chat_thread(sockfd);
    send_login(sockfd, username, password);
    while(!logged_in) {
        usleep(100 * 1000);   
    }
    chat_menu(sockfd);
}
