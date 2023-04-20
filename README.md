# Truss_Analyze-1.1
This project is created for the purpose of using by civil engineer students to help them about analysing of 2D truss systems by using stiffness matrix method .


You can use this python code to obtain the system's global stiffness matrix,displacements values for unconstrained nodes,support reactions and member's comprassion and tension values .


How to use ? Follow these steps :

1.First of all you should enter some values for the system in the input field which is loacated at the top of the code block .These ones:

                                  -elasticity  : it specifies the modulus of elasticity ( the code assumes all members have the same elasticity yet.)

                                  -areaSection : it specifies the cross section area of the members (  the code assumes all members have the same area 
                                                         section yet

                                  -numOfJoints: it specifies the total number of joints in the truss system 

                                  -numOfMembers:  it specifies the total number of members in the truss system

2.Then, the code will generate some quenstions to you .These ones:

                                   - " enter the n.joint NUMBER of the JOINT: " ( You have to name your joints on the system by number.You don't have to
                                        enter the same value with "n" here  but I suggest to do so.  Don't use comma between them.)
                                   
                                      " enter the NODE numbers of the n.JOINT formatted as x,y: " ( You have to specify two node numbers  which is 
                                        perpendicular to the xy axis for every joints arbitrarly. You should enter as x , y respectively .For example : " 2,3 " which 
                                        means x component of the joint is named as 2 and y component of the joint is named as 3 )

                                     " enter the LOCATION of the n. JOINT formatted as x,y: " (You have to specify the location of the joint as x,y 
                                        respectively.For example " 1,2" mean is x component of the joint is 1 and y component of the joint is 2. Don't use 
                                       comma between them.)

These questions will be repeat up to according to your answer at the inputs for variable numOfJoints

3.After that , the code will ask these questions : 

                                     " enter a SINGLE constrained NODE NUMBER (for quit q):" (You have to specify the constrained nodes which 
                                       correspond to support condition of the point . I didn't use such a pin or roller system to specify the node condition 
                                       because the purpose of creating the system flexibly.You can input so many entry for the supports that you desire to 
                                       give constrain  a single node , not node couple .For example if you entered "1" as an input that mean is asigned to the 
                                       node 1 a constrained.)

After defined constrained nodes you can input "q" as a value to quit this question loop.

4.Then, we will continue with these questions :

                                     " enter a single LOAD and it's corresponding NODE NUMBER as (x,y) (for quit q): " (To assign a load to a specifing joint 
                                       we will use joint's node numbers for convenience to implfy the load's direction . Positive values will indicate the same 
                                       direction with the node numbers , negative ones   opposite .Use first parameter for the load value and second one for 
                                       the node number. For example -1,4 will indicate the -1 load will influence at the joint which the node numbers 4 
                                       derivated and with the opposite direction to node number 4.After assigned all loads enter "q" as a input to quit the 
                                       question loop.)

                                     " enter a single DISPLACEMENT and it's corresponding NODE NUMBER as (x,y) (for quit q): " (To assign a displacement 
                                       to a specifing joint we will use joint's node numbers for convenience to implfy the displacement's direction . Positive 
                                       values will indicate the same direction with the node numbers , negative ones   opposite .Use first parameter for the 
                                       displacement value and second one for the node number. For example -0.04,4 will indicate the -0.04 displacement will 
                                       influence at the joint which the node numbers 4  derivated and with the opposite direction to node number 4.After 
                                       assigned all displacement enter "q" as a input to quit the  question loop.Be carefull when enter the displacement 
                                       values .You should always point instead of comma when you use a float number as enter.)

5.Latstly ,We will answer these questions : 

                                     "please select two joint from [joints] with dividing comma to draw a line between them :: " (To draw a line between the 
                                      joints we will select two joints which correspond to the first one is near  end and and the second one is far end of the 
                                      member.This question will repeat up to according to your input at the input field at the first step for variable 
                                      numOfMembers.An example for input at this question is "2,1" which means draw a line between joint 2 and 1, also 2 
                                      towards one and near end of the member will be 2 and far end the member will be one .)


After these five step the code will generate and create a graph of the system.Close the graph window and you will obtain the displacements , support reaction and member forces.

***The code can support these conditions:
                    
                  - Settled supports condition
                  - Truss under load , displacements or both of them
     
***The code can not support these conditions. I will work on these conditons to add the code :
                    
                  - Having inclined supports
                  - Having thermal expansion condition
                  - Having fabrication errors on the members
                  -Having  variable modulus of elasticity or cross sectional area members              
