#include <stdio.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define FEET_TO_METERS 0.3048f
#define POUNDS_TO_KILOGRAMS 0.4536f

typedef struct {
	unsigned id;
	float height;
	float weight;
	float accuracy;
} Clone;

Clone master_copy;

// Must be located at an address aligned by 16 bytes!
Clone* clone_army;
unsigned clone_army_count;


static char* read_line(void) {
	static char line_buffer[100];
	
	if (fgets(line_buffer, sizeof(line_buffer), stdin) == NULL) {
		printf("I'll be awaiting your return!\n");
		exit(EXIT_FAILURE);
	}
	
	char* p;
	for (p = line_buffer; *p != '\0'; p++) {
		if (*p == '\n') {
			*p = '\0';
			break;
		}
	}
	
	return line_buffer;
}

static char* vprompt_str(const char* prompt, va_list ap) {
	vprintf(prompt, ap);
	return read_line();
}

static char* prompt_str(const char* prompt, ...) {
	va_list ap;
	va_start(ap, prompt);
	return vprompt_str(prompt, ap);
}

static bool prompt_int(int* out, const char* prompt, ...) {
	va_list ap;
	va_start(ap, prompt);
	char* str = vprompt_str(prompt, ap);
	va_end(ap);
	
	return sscanf(str, "%d", out) == 1;
}

static bool prompt_float(float* out, const char* prompt, ...) {
	va_list ap;
	va_start(ap, prompt);
	char* str = vprompt_str(prompt, ap);
	va_end(ap);
	
	return sscanf(str, "%f", out) == 1;
}

static void configure_master_copy(void) {
	float v;
	
	printf("Excellent, let's start with the master clone's specs!\n");
	
	// Exploit: 0.0
	if (!prompt_float(&v, "Height (feet)?\n> ")) {
		goto bad;
	}
	master_copy.height = v * FEET_TO_METERS;
	
	// Exploit: Some small, nonzero int (bitwise cast to float)
	if (!prompt_float(&v, "Weight (pounds)?\n> ")) {
		goto bad;
	}
	master_copy.weight = v * POUNDS_TO_KILOGRAMS;
	
	// Exploit: 0.0
	if (!prompt_float(&v, "Accuracy (percent)?\n> ")) {
		goto bad;
	}
	master_copy.accuracy = v / 100.0f;
	return;
	
bad:
	printf("My liege, I am afraid I must be feeling unwell today.\n");
	exit(EXIT_FAILURE);
}

static void make_clones(void) {
	int n;
	if (
		!prompt_int(&n, "How many clones shall be produced, my liege?\n> ")
		|| n < 0
	) {
		printf("Please forgive me sir, as I'm afraid I do not posess the mental capacity to understand your request.\n");
		return;
	}
	
	unsigned additional_troops = (unsigned)n;
	
	if (additional_troops == 0) {
		printf("Understood, sir. No clones will be produced.\n");
		return;
	}
	
	// Integer overflow is not the intended vulnerability, so carefully ensure this won't overflow.
	unsigned old_count = clone_army_count;
	if (__builtin_uadd_overflow(old_count, additional_troops, &clone_army_count)) {
		printf("Sorry sir, but I can't produce that many clones.\n");
		exit(EXIT_FAILURE);
	}
	
	printf("Right away, sir!\n");
	
	// When requesting a large number of clones, this allocation request will fail and
	// return NULL.
	clone_army = realloc(clone_army, clone_army_count * sizeof(Clone));
	
	// Attacker can write a clone over top of both the `clone_army` pointer and the
	// `clone_army_count` variable. By corrupting the count variable to be relatively
	// small, this loop can be escaped safely.
	unsigned i;
	for (i = old_count; i < clone_army_count; i++) {
		// If `clone_army` is now NULL, this will write to an offset calculated by
		// `sizeof(Clone) * i`, which is a large number. An attacker can manipulate
		// clone production orders so that the offset lands at a corruption target
		// when they are ready to make the realloc fail.
		Clone* clone = &clone_army[i];
		
		// Each clone gets a unique id, which is the byte offset of the clone in the
		// clone army array. This is done so that when `clone_army` is NULL, the `id`
		// field will actually be a (32-bit) pointer to itself.
		clone->id = (char*)clone - (char*)clone_army;
		
		// By carefully configuring the master clone's contents, the attacker can
		// write controlled data to a controlled absolute address, resulting in a
		// write-what-where primitive.
		clone->height = master_copy.height;
		clone->weight = master_copy.weight;
		clone->accuracy = master_copy.accuracy;
	}
	
done:
	printf(
		"Your %u new clones are ready, bringing the army up to %u total clones!\n",
		additional_troops, clone_army_count
	);
}

static void customize_troops(void) {
	int n;
	if (
		!prompt_int(&n, "Which soldier requires corrective action, my liege?\n> ")
		|| n < 0
		|| n % sizeof(Clone) != 0
		|| n / sizeof(Clone) >= clone_army_count
	) {
		printf("Respectfully, sir, we don't have a soldier with that ID...\n");
		exit(EXIT_FAILURE);
	}
	
	Clone* clone = &clone_army[n / sizeof(Clone)];
	// if(clone->id != n) {
	// 	printf("We already corrected that soldier, sir.\n");
	// 	exit(EXIT_FAILURE);
	// }
	
	do {
		if (
			!prompt_int(
				&n,
				"Which of soldier #%u's attributes would you like to change?\n"
				"[1] ID\n"
				"[2] Height\n"
				"[3] Weight\n"
				"[4] Accuracy\n"
				"> ",
				clone->id)
			|| n < 1
			|| n > 4
		) {
			goto bad;
		}
		
		switch (n) {
			case 1:
				if (
					!prompt_int(&n, "New ID?\n> ")
					|| n < 0
				) {
					goto bad;
				}
				
				// Sample address of system(): 0x7ffff7dd9d70
				// Low 32 bits of that are 0xf7dd9d70, which is negative and therefore
				// invalid as an ID. Attacker will need to use one of the float fields
				// to build the low 32 bits of a libc address.
				clone->id = n;
				break;
			
			case 2:
				if (!prompt_float(&clone->height, "New height (feet)?\n> ")) {
					goto bad;
				}
				clone->height *= FEET_TO_METERS;
				break;
			
			case 3:
				if (!prompt_float(&clone->weight, "New weight (pounds)?\n> ")) {
					goto bad;
				}
				clone->weight *= POUNDS_TO_KILOGRAMS;
				break;
			
			case 4:
				if (!prompt_float(&clone->accuracy, "New accuracy (percent)?\n> ")) {
					goto bad;
				}
				clone->accuracy /= 100.0f;
				break;
		}
		
		if (!strcmp(prompt_str("Are you satisfied with these corrections?\n> "), "yes")) {
			break;
		}
	} while(true);
	
	return;
	
bad:
	printf("I... uhm... understand. Right. Of course, sir.\n");
	exit(EXIT_FAILURE);
}

int main(void) {
	char* response = prompt_str("Supreme commander! Are you ready to build our clone army?\n> ");
	if (strcmp(response, "yes")) {
		printf("I see, my liege. I will await your orders.\n");
		return 0;
	}
	
	configure_master_copy();
	
	do {
		response = prompt_str("Shall we make %s clones?\n> ",
			clone_army_count == 0 ? "some" : "more"
		);
		
		if (strcmp(response, "yes")) {
			break;
		}
		
		make_clones();
	} while(1);
	
	if (clone_army_count == 0) {
		printf("Find me when you're ready to build the clone army, sir.\n");
		return 0;
	}
	
	do {
		response = prompt_str("Oh glorious one, are there any soldiers you're unsatisfied with?\n> ");
		
		if (strcmp(response, "yes")) {
			printf("Wonderful!\n");
			break;
		}
		
		customize_troops();
	} while(1);
	
	printf("Your clone army is ready to conquer the galaxy, my liege!\n");
	return 0;
}
