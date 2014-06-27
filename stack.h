/*
memory allocation too
*/
#ifndef __STACK_H__
#define __STACK_H__

#include "stdint.h"

#define STACK_SIZE 0x1000

extern uint8_t mem_pool[];  /*the static memory pool. All the memory blocks being malloc are in here.*/

struct mem_block_node
{
	struct mem_block_node *prev_node;
	struct mem_block_node *next_node;
	uint16_t size;
	uint8_t *data;
};

void test();


#endif /* __STACK_H__ */