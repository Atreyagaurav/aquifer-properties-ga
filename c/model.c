#include "model.h"
#include <stdio.h>
#include <stdlib.h>

const int obs_data_rows=20;
const int obs_data_cols=2;

const int THEIS_MAX_ITERATIONS=10;
const double THEIS_CALC_LIMIT=1e-5;
const double Q=8.155;
const double r=582;

/* time,drawdown */
const double obs_data[] = {
  1.93, 0.11,
  2.98, 0.14,
  4.00, 0.15,
  5.12, 0.18,
  5.95, 0.20,
  6.88, 0.22,
  8.05, 0.23,
  8.88, 0.24,
  10.97, 0.27,
  12.73, 0.29,
  14.73, 0.31,
  17.75, 0.34,
  35.22, 0.40,
  41.41, 0.42,
  53.65, 0.45,
  59.51, 0.47,
  97.06, 0.53,
  117.06, 0.54,
  193.64, 0.59,
  280.46, 0.64,
};


double calculate_mae(double *simulated){
  double mae=0;
  int i;
  for(i=0;i<obs_data_rows;i++){
    mae += fabs(*(simulated+i) - *(obs_data+obs_data_cols*i+1));
  }
  mae /= obs_data_rows;
  return mae;
}


double calculate_mae_ST(double S, double T){
  double mae=0;
  int i;
  double coeff_srt, coeff_ut;
  coeff_srt = Q / (4 * M_PI * T);
  coeff_ut = r * r * S / (4 * T);
  for(i=0;i<obs_data_rows;i++){
    mae += fabs(coeff_srt *
		calculate_wu(coeff_ut/
			     *(obs_data+obs_data_cols*i))
		- *(obs_data+obs_data_cols*i+1));
  }
  mae /= obs_data_rows;
  return mae;
}

void calculate_drawdowns(double S, double T, double *target){
  double coeff_srt, coeff_ut, wu;
  coeff_srt = Q / (4 * M_PI * T);
  coeff_ut = r * r * S / (4 * T);
  int i;
  for(i=0; i<obs_data_rows; i++){
    wu = calculate_wu(coeff_ut/
		      *(obs_data+obs_data_cols*i)); /* ut/t */
    *(target+i)= coeff_srt * wu;
  }
}

double calculate_wu(double u){
  double wu = -log(u) - 0.57721;
  double term = (u);
  int i=2;
  do{
    wu += term;
    term *= -(u/i)*(i-1)/i;
    i++;
  }while(term>THEIS_CALC_LIMIT || i<THEIS_MAX_ITERATIONS);
  return wu;
}

/* int main(int argc, char *argv[]) */
/* { */
/*   if (argc <2) return 0; */
/*   double S,T; */
/*   S = atof(argv[1]); */
/*   T = atof(argv[2]); */
/*   double drawdowns[22]; */
/*   calculate_drawdowns(S, T, drawdowns); */
/*   printf("S=%f\nT=%f\n", S, T); */
/*   printf("MAE: %f", calculate_mae(drawdowns)); */
/*   int i; */
/*   for(i=0; i<obs_data_rows; i++){ */
/*     printf("\n%f",*(drawdowns+i)); */
/*   } */
/*   printf("\n"); */
/*   return 0; */
/* } */
