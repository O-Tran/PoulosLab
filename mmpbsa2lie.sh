#!bin/bash
echo "  "
echo "  "
echo "Useage: input_normal_mmgbsa input_mmgbsa_with_protein_charges_off  output_dGlie_file "
echo "  "
echo "Input normal mmgbsa file                                $1"
echo "Input mmgbsa file with protein charges zero in receptor $2"
echo "Output Deltag G file                                    $3"
echo "   "
#This script takes output from MMGBSA and calculates a LIE energy
# See Carlsson et al (2006) J. Phys. Chem 110, 12034
# The electrostatic terms in COM-REC + 2*LIGbound - 2*LIGfree
# COM-REC is just the difference in EEL between COM and REC. LIGbound
# is the GB reaction field solvation energy of the ligand bound to the protein.
# This is computed by setting the protein charges to zero in the MMGBSA calculation
# for the receptor. LIGfree is just the GB reaction field foe ligand alone
# VDW is just the usual COM-LIG-LIG plus GBSUR (nonpolar solvation energy).
# which is the reaction field. 
####the final dGlie= 0.50(deltatEEL + 0.18(VdeltatDW)
####complex-receptor-ligand EEL#######
grep ELE $1 > tempa
sed '2,4d' tempa > tempb
awk '{dif=$2-$4} END {print dif}' tempb > tempELEcom-rec
sed '1,2d' tempa > tempb
sed '$d' tempb > tempc
awk '{print $2}' tempc > temp_com-rec_EEL
####get the GB for ligand bound to protein########
grep "GB " $2 > tempa
sed '2d' tempa > tempb
#awk '{dif=$2-$4} END {print dif}' tempb > tempGBligand_bound
awk '{print $4}' tempb > tempGBligand_bound
############get the GB for the ligand alone##########
grep "GB " $1  > tempa
sed '2d' tempa > tempb
awk '{print $6}' tempb > tempGBligand_free
###########aseemble electrostatic part###########
paste tempELEcom-rec tempGBligand_bound tempGBligand_free >  tempEELall
awk '{sum=$1+2*$2-2*$3} END {print sum}' tempEELall > tempDeltaEEL
###################get VDW and GBSUR terms###########
grep VDW $1 > tempa
sed '1d' tempa > tempb
awk '{print $2}' tempb > tempDeltaVDW
grep GBSUR $1 > tempa
sed '1d' tempa > tempb
awk '{print $2}' tempb > tempDeltaGBSUR
###########assemble VDW and GBSUR########
paste tempDeltaVDW tempDeltaGBSUR> tempDeltatVDW_GBUSR
awk '{sum = $1+$2} END {print sum}' tempDeltatVDW_GBUSR > tempDeltatVDW+GBSUR
###########assemble EEL and VDW for final calculation##################
paste tempDeltaEEL tempDeltatVDW+GBSUR > tempa
awk '{sum = 0.50*$1 + 0.18*$2}; END {print "dGlie = " sum}' tempa > $3 
rm temp*
