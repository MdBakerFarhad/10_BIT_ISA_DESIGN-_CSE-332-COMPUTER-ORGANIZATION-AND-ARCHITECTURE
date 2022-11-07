#GROUP 01
#1. Abid Ahsan Shanto - 1921738042
#2. Md. Baker - 1911672642
#3. Mariya Sharmin Tisha - 1911637642
class Assembler:

     #returns the 2's complement of a binary string in n bit representation
     def two_complement(self,bin_1,bits_1):
          dict_p = {"0":"1","1":"0"}                           
          result = ''.join(dict_p[x] for x in bin_1)
          two_c = bin((int(result,2)+1))[2:].zfill(bits_1)
          return two_c

     #returns binary for constant values in n bit representation
     def get_bin_for_integer(self,string1,bits):
          int_v = int(string1)
          get_binary = lambda x,n: format(x,"b").zfill(n)
          bin_val = get_binary(int_v,bits)
          return bin_val
     
     # function for extracting operator, if valid not found
     #return string error and prompt a command
     def Extract_operator(self,op_name):
          op_bin =""
          if op_name.lower() == "add": # 0
               op_bin = "0000"
          elif op_name.lower() == "sub": #1
               op_bin = "0001"  
          elif op_name.lower() == "addi": #2
               op_bin = "0010"
          elif op_name.lower() == "lw": #3
               op_bin = "0011"
          elif op_name.lower() == "sw": #4
               op_bin = "0100"
          elif op_name.lower() == "beqz":#5
               op_bin = "0101"
          elif op_name.lower() == "bgtz":#6
               op_bin = "0110"
          elif op_name.lower() == "bltz":#7
               op_bin = "0111"
          elif op_name.lower() == "bnez":#8
               op_bin = "1000"
          elif op_name.lower() == "bgez":#9
               op_bin = "1001"
          elif op_name.lower() == "j":#a
               op_bin = "1010"
          elif op_name.lower() == "and":#b
               op_bin = "1011"
          elif op_name.lower() == "or":#c
               op_bin = "1100"
          elif op_name.lower() == "nor":#d
               op_bin = "1101"
          elif op_name.lower() == "in":#e
               op_bin = "1110"
          elif op_name.lower() == "out":#f
               op_bin = "1111"
          else:
               op_bin = "error"
               #print("Invalid operation. Check the mips instruction set!!")
          
          return op_bin

     #check whether the string passed is a register
     def check_register(self,reg_name):
          if '$' in reg_name:
               return True
          else:
               return False

     #Extract the register binary value
     def Extract_register(self,reg_name):
          reg_bin = ""
          if reg_name.lower() == "$zero": # 0
               reg_bin = "000"
          elif reg_name.lower() == "$s0": # 1
               reg_bin = "001"
          elif reg_name.lower() == "$s1": #2
               reg_bin = "010"
          elif reg_name.lower() == "$s2": #3
               reg_bin = "011"
          elif reg_name.lower() == "$s3": #4
               reg_bin = "100"
          elif reg_name.lower() == "$t0": #5
               reg_bin = "101"
          elif reg_name.lower() == "$t1": #6
               reg_bin = "110"
          elif reg_name.lower() == "$t2":
               reg_bin = "111" # t2 = 7
          
          return reg_bin
          
     #Assembles the mips to hex code writes to file
     def assemble_code(self):
          with open("input.txt","r") as freader:
               lines = freader.readlines()
          fwriter = open("output.txt","w")

          for x in lines:
               sp = x.strip().split(" ")
               
               #operand fetched
               operator = sp[0]
               if self.Extract_operator(operator) == "error":
                    print(operator + " Invalid operation. Check the mips instruction set!!")
                    break
               else:
                    l_r0 = self.Extract_operator(operator)
                   # l_r0 = hex(int(self.Extract_operator(operator),2))[2:]
               
               #second target or register fetch
               reg_im1 = sp[1]
               if operator.lower()!="j" and self.check_register(reg_im1):
                    if operator.lower() == "in" or operator.lower() == "out":
                         try:
                              l_r1 = "000" + self.Extract_register(reg_im1)
                              #l_r1 = hex(int(self.Extract_register(reg_im1),2))[2:]
                         except ValueError:
                              print(reg_im1 + " is not a valid register")
                              break
                    else:
                         try:
                              l_r1 = self.Extract_register(reg_im1)
                              #l_r1 = hex(int(self.Extract_register(reg_im1),2))[2:]
                         except ValueError:
                              print(reg_im1 + " is not a valid register")
                              break
               elif operator.lower() =="j" and self.check_register(reg_im1):
                    print("Operator J only has a target constant as operand")
                    break
               elif operator.lower()!="j" and self.check_register(reg_im1)==False: 
                    print("R type and I type must have atleast 1 register type operand")
                    break
               else:
                    try:
                         if int(reg_im1) < 0:
                              get_bin = self.get_bin_for_integer(reg_im1.strip("-"), 6)
                              get_2_bin = self.two_complement(get_bin, 6)
                              l_r1 = get_2_bin
                              #l_r1 = hex(int(get_2_bin,2))[2:]
                         else:
                              get_bin = self.get_bin_for_integer(reg_im1, 6)
                              l_r1 = get_bin
                              #l_r1 = hex(int(get_bin,2))[2:]
                    except ValueError:
                         print("Neither a register or target or immediate")
                         break

               # third register/null/constant fetch
               if operator.lower() == "in" or operator.lower() == "out" or operator.lower() == "j":
                    l_r2 = " "
               else:
                    reg_im2 = sp[2]
                    if (operator.lower() =="add" or operator.lower() == "sub" or operator.lower() == "and" or operator.lower() == "or" or operator.lower() == "nor") and self.check_register(reg_im2):
                         try:
                              l_r2 = self.Extract_register(reg_im2)
                              #l_r2 = hex(int(self.Extract_register(reg_im2),2))[2:]
                         except ValueError:
                              print( reg_im2 + " Not a valid register")
                              break
                    elif (operator.lower() =="add" or operator.lower() == "sub" or operator.lower() == "and" or operator.lower() == "or" or operator.lower() == "nor") and self.check_register(reg_im2)== False:
                         print("R type operations only have register as operands")
                         break
                    elif (operator.lower() !="add" or operator.lower() != "sub" or operator.lower() != "and" or operator.lower() != "or" or operator.lower() != "nor") and self.check_register(reg_im2)== False:
                         try:
                              if int(reg_im2) < 0:
                                   get_bin1 = self.get_bin_for_integer(reg_im2.strip("-"), 3)
                                   get_2_bin1 = self.two_complement(get_bin1, 3)
                                   l_r2 = get_2_bin1
                                   #l_r2 = hex(int(get_2_bin1,2))[2:]
                              else:
                                   get_bin1 = self.get_bin_for_integer(reg_im2, 3)
                                   l_r2 = get_bin1
                                   #l_r2 = hex(int(get_bin1,2))[2:]
                         except ValueError:
                               print("Neither a register or an immediate")
                               break
                    else:
                         print("I Type must have an immediate as an operand")
                         break
               f_string = l_r0 + l_r1 + l_r2
               f_code = '%.*x' % (3, int('0b'+f_string, 0))
               fwriter.write(f_code + "\n")
               


          freader.close()
          fwriter.close()
          
if __name__ == "__main__":
     a = Assembler()
     a.assemble_code()

     