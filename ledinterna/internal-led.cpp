#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// Define o pino do LED interno
#define LED_BUILTIN GPIO_NUM_2  // GPIO 2 é o LED embutido na maioria das ESP32

extern "C" void app_main() {
    // Reseta o pino para seu estado inicial
    gpio_reset_pin(LED_BUILTIN);

    // Configura o pino como saída
    gpio_set_direction(LED_BUILTIN, GPIO_MODE_OUTPUT);

    while (true) {
        // Acende o LED
        gpio_set_level(LED_BUILTIN, 1);
        printf("LED ON\n");
        vTaskDelay(1000 / portTICK_PERIOD_MS);  // Atraso de 1 segundo

        // Apaga o LED
        gpio_set_level(LED_BUILTIN, 0);
        printf("LED OFF\n");
        vTaskDelay(1000 / portTICK_PERIOD_MS);  // Atraso de 1 segundo
    }
}
