#
print ("TTL2-modeling-trial00")
print (" {180227}, {180303} ")
print (" coded by M Kinoshita ")
"""
At boundary 境界の上では

    dEnergy_bndry
    dMass_bndry
    velocity_bndry
    Area_bndry

At segment Volume セグメント体積の中では

    Energy_seg
    TdegC_seg 温度℃
    Density_seg 密度
    CpHeat_seg
    Vol_seg
    dX_seg  セグメントのｘ方向の長さ

At wall 
    
    file:///Users/moto/Downloads/simulation_of_flow_of_TTL_180227.html
"""
Time = 0 #time indication
N=13  #temporarily number of segment volume is 13
dEnergy_bndry=dMass_bndry=velocity_bndry=Area_bndry=[0]*N
dEnergy_wall=[0]*N
#>>
Energy_seg=TdegC_seg=Density_seg=CpHeat_seg=Volume_seg=[0]*N
dEnergy_seg=[0]*N
#>
# Followings are initial conditions
dEnergy_wall=[10,0,0,0,0,0,0,0,0,0,0,0,0] # 0=Core with heat source 
TdegC_seg=[600]*N
TdegK_seg=[600+273.15]*N
Vol_seg=[1]*N  # in real case it is order of 10*1E-6 (m^3)
velocity_bndry=[0]*N
velocity_bndry[3]=1.0  # segment 3 is pump for this case.
Mass_seg=[1]*N
dMass_seg=[0]*N
Density=[1]*N
Area_bndry=[1]*N
# Physical constants
CpHeat_seg=[1.0]*N  #heat capacity of FLiNaK is  
#>>
print (dEnergy_bndry)
dTime=0.1
#>>
#Updating: {increment of Energy}, dEnergy, {increment of Mass}, dMass
#Here, i is an index of each cell (volume segment), 
#t is a time, and dt is the time step.


#Pseudo Code by Chiba-san
#{increment of Energy in Segment Volume}(i) 
#   =Energy_seg(i)_{t+dt}- Energy_seg(i)_{t}
#   =dEnergy_bndry(i)-dEnergy_bndry(i+1)+{Calorie from wall}(i)
#   =dEnergy_bndry(i)-dEnergy_bndry(i+1)+dEmergy_wall(i)
for i in range(0,N):
  if velocity_bndry[i] >= 0:
    dEnergy_bndry[i] = (
(Density_seg[i-1]*CpHeat_seg[i-1]*TdegC_seg[i-1])*(velocity_bndry[i]*Area_bndry[i])*dTime  ) 
    #OBS!  continuous line is made by ()
  else:    #if velocity(i)<0
    dEnergy_bndry[i] = (
       -(Density_seg[i]* CpHeat_seg[i]* TdegC_seg[i])
          *(velocity_bndry[i]* Area_bndry[i])*dTime  )
  if velocity_bndry[i]>=0 :
    if (i+1)==N:
      dEnergy_bndry[0] = (
        (Density_seg[i]* CpHeat_seg[i]* TdegC_seg[i])
       *(velocity_bndry[0]* Area_bndry[0])*dTime   )
    else:
      dEnergy_bndry[i+1] = (
        (Density_seg[i]* CpHeat_seg[i]* TdegC_seg[i])
       *(velocity_bndry[i+1]* Area_bndry[i+1])*dTime   )
  else:
    if (i+1)==N:
       dEnergy_bndry[0] = (
       -(Density_seg[i]* CpHeat_seg[i]* TdegC_seg[i])
        *(velocity_bndry[i]* Area_bndry[i])* dTime   )
       dEnergy_seg[i]= (dEnergy_bndry[i] - dEnergy_bndry[0] 
               + dEnergy_wall[i] )    # Energy in/out through wall
    else:
      dEnergy_bndry[i+1] = (
       -(Density_seg[i]* CpHeat_seg[i]* TdegC_seg[i])
        *(velocity_bndry[i]* Area_bndry[i])* dTime   )
      dEnergy_seg[i]= (dEnergy_bndry[i] - dEnergy_bndry[i+1] 
               + dEnergy_wall[i] )    # Energy in/out through wall
#{increment of Mass}(i) = dMass(i)-dMass(i+1),
  if velocity_bndry[i]>=0 :
     dMass_bndry[i] = ( Density_seg[i-1]
                         *(velocity_bndry[i]* Area_bndry[i]) )
  else:
     dMass_bndry[i] = -( Density_seg[i]*(velocity_bndry[i]*Area_bndry[i])*dTime )
  if velocity_bndry[i]>0 or velocity_bndry[i] ==0 :
    if(i+1)==N:
     dMass_bndry[0]  =(Density_seg[i]*(velocity_bndry[0]*Area_bndry[0])*dTime )
    else:
         dMass_bndry[i+1]  =(Density_seg[i]*(velocity_bndry[i+1]*Area_bndry[i+1])*dTime )

  else:
    if(i+1)==N:
         dMass_bndry[0] = (
         Density_seg[0]*(velocity_bndry[0]* Area_bndry(i+1))*dTime ) 
    else:
     dMass_bndry[i+1] = (
         Density_seg(i+1)*(velocity_bndry(i+1)* Area_bndry(i+1))* dTime )
#>>
    if i+1==N: dMass_seg[i] = dMass_bndry[i] - dMass_bndry[0]
    else: dMass_seg[i] = dMass_bndry[i] - dMass_bndry[i+1]
#>>
#>>
# flow velocity is indiced by Mass increment and overflow from the
# segment volume.
# dVolume=Mass/Density-Volume(previous)
# velocity = dVolume/Area
  dVolume=Mass_seg[i] + dMass_seg[i]/Density[i]
  if velocity_bndry[i]>0 or velocity_bndry[i] ==0 :
    if (i+1)==N: velocity_bndry[0] = dVolume/Area_bndry[0]
    else: velocity_bndry[i+1] = dVolume/Area_bndry[i+1]
  else: velocity_bndry[i] = dVolume/Area_bndry[i]
# 千葉さん、流速の計算をここに置くのが良いかは、まだわかりません。
# Change of Temperature and Density induces net transfer through boundary
# Discuss place of the following statement wether at the end of loop 
# or beginning of loop or inside of the increment equations.
Energy_seg[i]+=dEnergy_seg[i]
Mass_seg[i]+=dMass_seg[i] 
#>>
#E=Density*Cp*T
Density_seg[i]=Mass_seg[i]/Vol_seg[i]
TdegK_seg[i]=Energy_seg[i]/(Density_seg[i]*CpHeat_seg[i])
#>>         
#"""     
#>>
# Loop of senments ends here
#i+=1
# 千葉さん、for文で、segmentを、ここまでで回してください。
# 最後には、円環を閉じてください。
# セグメント0へと。。
# Loop of time step
#　千葉さん、適当に時間を進めてください。20回ぐらい繰り返せば・・・
#Time+=dTime
# End of program