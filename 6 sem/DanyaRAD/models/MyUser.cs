using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Net.Mime.MediaTypeNames;

namespace DanyaRAD.models
{
    internal class MyUser
    {
        public String fio { get; set; }
        public String address { get; set; }
        public String city { get; set; }
        public int sex { get; set; }
        public List<String> hobbies { get; set; }
        public MyUser(string fio=null, string address=null, string city=null, int sex=0, List<string> hobbies=null)
        {
            this.fio = fio;
            this.address = address;
            this.city = city;
            this.sex = sex;
            this.hobbies = hobbies;
        }

        public String getInfo()
        {
            String info = "";
            info += "ФИО: " + this.getfio() + "\n";
            info += "Адрес: " + this.getaddress() + "\n";
            if (this.getsex() == 1)
                info += "Пол мужской\n";
            else if (this.getsex() == 2)
                info += "Пол женский\n";
            else
                info += "Пол другое\n";

            info += "Секции: ";
            for (int i = 0; i < hobbies.Count; i++) {
                info += hobbies[i] + " ";
            }
            info += "\n";

            return info;
        }

        public void addHobby(String hobby) { this.hobbies.Add(hobby); }

        public String getfio() { return fio; }
        public String getaddress() { return address; }
        public String getcity() { return city; }
        public int getsex() { return sex; }
        public List<String> getHobbies() { return hobbies; }

        public void setFio(String fio) { this.fio = fio; }
        public void setaddress(String address) { this.address = address; }
        public void setcity(String city) { this.city = city; }
        public void setsex(int sex) { this.sex = sex; }
        public void setHobbies(List<String> hobbies) { this.hobbies = hobbies; }

    }
}
