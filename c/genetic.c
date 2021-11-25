#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "model.h"

const int genome_length=75;
const int num_para=2;
const int mutation_chance=5;
const int gene_length=genome_length*num_para;
const int crossover_genes=gene_length/4;
const int crossover_repeat=2;
const int population=1000;
const int elite_choice=population/4;
const int generations=1000;

#define PARA_MAX_LOG_S -2
#define PARA_MIN_LOG_S -14
#define PARA_MAX_LOG_T 3
#define PARA_MIN_LOG_T -3

void print_gene(_Bool* gene){
  int i;
  /* char *gene_str = malloc(sizeof(char)*genome_length); */
  for (i=0; i<gene_length; i++){
    putchar('0' + *(gene+i));
  }
}

void random_gene(_Bool* gene){
  int i;
  /* char *gene_str = malloc(sizeof(char)*genome_length); */
  for (i=0; i<gene_length; i++){
    *(gene+i) = random()>(RAND_MAX/2)?1:0;
  }
}

void fill_gene(_Bool* gene, _Bool value){
  int i;
  /* char *gene_str = malloc(sizeof(char)*genome_length); */
  for (i=0; i<gene_length; i++){
    *(gene+i) = value;
  }
}

void custom_gene(_Bool* gene, char * gene_str){
  int i;
  /* char *gene_str = malloc(sizeof(char)*genome_length); */
  for (i=0; i<gene_length; i++){
    *(gene+i) = *(gene_str+i)-'0';
  }
}

void mutate_gene(_Bool* gene){
  int i;
  /* char *gene_str = malloc(sizeof(char)*genome_length); */
  for (i=0; i<gene_length; i++){
    if (random()%100 < mutation_chance){
    *(gene+i) = 1 - *(gene+i);
    }
  }
}

double decode_genome(_Bool *gene){
  double val=1.0/(pow(2, genome_length));
  double factor=0.5;
  int i;
  for(i=0; i<genome_length; i++){
    if (*(gene+i)) {
      val += factor;
    }
    factor /= 2;
  }
  return val;
}

double get_parameter(_Bool *gene, double min, double max, int index){
  /* index = 0 for storativity, 1 for transmissivity */
  double factor = decode_genome(gene + index*genome_length);
  double real_factor = (max-min)*factor + min;
  return pow(10, real_factor);
}

void crossover(_Bool *gene1, _Bool* gene2, _Bool *target){
  int i, j;
  for(i=0; i<gene_length; i++){
    *(target+i) = *(gene1+i);
  }
  
  for(j=0; j< crossover_repeat; j++){
  int pos = random()%gene_length;
  for(i=0; i<crossover_genes; i++){
    pos = (pos+1)%gene_length;
    *(target + pos) = *(gene2+pos);
  }}
}

void sort_genes(_Bool *genes, int *index){
  double *mae = malloc(population*sizeof(double));
  int i;
  double S, T;
  
  for(i=0; i<population; i++){
    S = get_parameter(genes+i*gene_length, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
    T = get_parameter(genes+i*gene_length, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
    *(mae+i) = calculate_mae_ST(S, T);
    }
  
  int cmpfunc (const void * a, const void * b) {
    return ( *(mae + *(int*)a) > *(mae + *(int*)b) ? 1 : -1 );
  }

  qsort(index, population, sizeof(int), cmpfunc);
  
}

void initialize_population(_Bool *genes){
  int i;
  for(i=0; i<population; i++){
    /* fill_gene(genes+i*gene_length, 0); */
    random_gene(genes + i);
  }
  /* custom_gene(genes+0*gene_length, "1101001101001110001010100010100100000000"); */
  /* custom_gene(genes+1*gene_length, "0110000001110000000011000100001000001000"); */
  /* custom_gene(genes+2*gene_length, "1011101010010101111110101101001111111011"); */
  /* custom_gene(genes+3*gene_length, "1100111001110010111110100011010010011010"); */
}

void print_population(_Bool *genes, int *index){
  double S,T;
  int i;
  _Bool *gene;
  for(i=0; i<population; i++){
    gene = genes+ *(index+i) * gene_length;
    S = get_parameter(gene, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
    T = get_parameter(gene, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
    print_gene(gene);
    printf(" || S: %e", S);
    printf(" || T: %f", T);
    printf(" || mae: %f\n", calculate_mae_ST(S, T));
  }
  printf("--------\n");
}

void save_population(_Bool *genes, int count){
  double S,T;
  int i;
  _Bool *gene;
  char filename[20];
  sprintf(filename, "./data/gen-%04d.txt", count);
  FILE *fp = fopen(filename, "w");
  for(i=0; i<population; i++){
    gene = genes+i*gene_length;
    S = get_parameter(gene, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
    T = get_parameter(gene, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
    fprintf(fp, "%e %f %f\n", S, T, calculate_mae_ST(S, T));
  }
  fclose(fp);
}

void print_population_mae(_Bool *genes, int *index){
  double S,T;
  int i=0;
  _Bool *gene;
  gene = genes+ *(index+i) *gene_length;
  S = get_parameter(gene, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
  T = get_parameter(gene, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
  /* print_gene(gene); */
  printf(" %e", S);
  printf(" %f", T);
  printf(" %f\n", calculate_mae_ST(S, T));
}

int get_random_elite(){
  int rint;
  rint = random() % elite_choice;
  
  return rint;
}

_Bool *next_generation(_Bool *genes, int* index){
  int i, j, c;
  _Bool *new_genes = malloc(population * gene_length * sizeof(_Bool));
  for (c=0; c<population; c++){
    i = get_random_elite();
    j = get_random_elite();
    crossover(genes + *(index+i) * gene_length,
	      genes + *(index+j) * gene_length,
	      new_genes + c * gene_length);
    mutate_gene(new_genes + c * gene_length);
  }
  free(genes);
  return new_genes;
}


int main(int argc, char *argv[])
{
  srand(time(NULL));
  /* int i, len = strlen(argv[1]); */
  _Bool *genes = malloc(population * gene_length * sizeof(_Bool));
  int *index = malloc(population*sizeof(int));
  int i;
  for(i=0; i<population; i++){
    *(index+i) = i;
  }
  initialize_population(genes);
  sort_genes(genes, index);
  /* print_population(genes, index); */
  for (i =0; i<generations;i++){
    printf("%d ", i);
    genes = next_generation(genes, index);
    sort_genes(genes, index);
    print_population_mae(genes, index);
    save_population(genes, i);
  }
  return 0;
}

