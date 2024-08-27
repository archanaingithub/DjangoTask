class Houser:
    window = 10
    color = "red"
  
    def set_color(self, color):
        self.color=color
        
    def get_color(self,color):
        return self.color


ram_ko_ghar = Houser()
print(ram_ko_ghar.color)
ram_ko_ghar.set_color("green")

print(ram_ko_ghar.color)
# shyam_ko_ghar.color = "purple"
# print(shyam_ko_ghar.color)
