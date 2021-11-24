#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "model.h"

const int genome_length=200;
const int num_para=2;
const int mutation_chance=1;
const int gene_length=genome_length*num_para;
const int crossover_genes=gene_length/2;
const int population=100;

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
  double val=1.0/(1<<genome_length);
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
  int pos = random()%gene_length;
  int i;
  for(i=0; i<gene_length; i++){
    *(target+i) = *(gene1+i);
  }
  for(i=0; i<crossover_genes; i++){
    *(target + (pos+i)%gene_length) = *(gene2+(i+pos)%gene_length);
  }
}

void calculate_errors();

void sort_genes(_Bool *genes, int *index){
  double *mae = malloc(population*sizeof(double));
  int i;
  double S, T;
  
  for(i=0; i<population; i++){
    S = get_parameter(genes+i, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
    T = get_parameter(genes+i, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
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
    random_gene(genes + i);
  }
}

void print_population(_Bool *genes, int *index){
  double S,T;
  int i;
  _Bool *gene;
  for(i=0; i<population; i++){
    gene = genes+ *(index+i);
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
    gene = genes+i;
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
  gene = genes+ *(index+i);
  S = get_parameter(gene, PARA_MIN_LOG_S, PARA_MAX_LOG_S, 0);
  T = get_parameter(gene, PARA_MIN_LOG_T, PARA_MAX_LOG_T, 1);
  /* print_gene(gene); */
  printf(" || S: %e", S);
  printf(" || T: %f", T);
  printf(" || mae: %f\n", calculate_mae_ST(S, T));
}

_Bool *next_generation(_Bool *genes, int* index){
  int i,j,c;
  _Bool *new_genes = malloc(population * gene_length * sizeof(_Bool));
  for (c=0; c<population;c++){
      i = random()%30;
      j = random()%30;
      crossover(genes+ *(index+i), genes + *(index+j), new_genes+c);
      mutate_gene(new_genes+c);
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
  for (i =0; i<2000;i++){
    printf("%d : ", i);
    genes = next_generation(genes, index);
    sort_genes(genes, index);
    print_population_mae(genes, index);
    save_population(genes, i);
  }
  return 0;
}

