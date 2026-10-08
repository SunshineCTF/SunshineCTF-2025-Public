#include <stdio.h>
#include <string.h>
#include <time.h>

struct satellite_status {
    int battery_level;
    int orbit_count;
    int temperature;
    time_t current_time;
};

int check_transmission_window(struct satellite_status *sat) {
    if (sat->battery_level > 75 &&
        sat->orbit_count % 16 == 0 &&
        sat->temperature < -20) {
        return 1;
    }
    return 0;
}

int main() {
    char flag[50];
    sprintf(flag, "sun{%s_%s_%s}\n", "e4sy", "s4t3ll1t3", "3131");

    struct satellite_status sat = {80, 32, -25, time(NULL)};
    char input[50];
    
    printf("Satellite Status: Battery=%d%%, Orbit=%d, Temp=%dC\n", 
           sat.battery_level, sat.orbit_count, sat.temperature);
    
    if (!check_transmission_window(&sat)) {
        printf("Transmission window closed. Access denied.\n");
        return 1;
    }
    
    printf("Enter satellite command: ");
    fgets(input, sizeof(input), stdin);
    
    if (strcmp(input, flag) == 0) {
        printf("Access Granted!\n");
    } else {
        printf("Access Denied!\n");
    }
    return 0;
}
