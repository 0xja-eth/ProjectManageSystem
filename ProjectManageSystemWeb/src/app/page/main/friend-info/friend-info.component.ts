import {Component, OnInit} from '@angular/core';
import {isEmpty} from "rxjs/operators";


@Component({
  selector: 'app-friend-info',
  templateUrl: './friend-info.component.html',
  styleUrls: ['./friend-info.component.css']
})
export class FriendInfoComponent implements OnInit {

  private instanceInfo: FriendInfo;
  private searchInput: string;
  friendsData: FriendInfo[] = randomData(20);
  searchData: FriendInfo[];

  // private Groups: Group[] = Group.Groups;
  constructor() {

  }

  ngOnInit() {
    // 生成数据并进行排序

    this.friendsData = randomData(30);
    this.friendsData = this.friendsData.sort( (a, b) => {
      return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
    });
    this.instanceInfo = this.friendsData[0];
  }

  // initGroups(): void{
  //   const sel = document.getElementById("groups");
  //   let str = "";
  //   for (const groupItem of Group.Groups) {
  //     str += '<option>' + groupItem.value + '</option>';
  //     console.log(str);
  //   }
  //   console.log("最后的" + str);
  //   sel.innerHTML = str;
  // }


  searchFriend(): FriendInfo[] {
    if (this.searchInput === undefined || this.searchInput === "") {
      this.searchData = [];
      document.getElementById("notice1").hidden = true;
      return;
    }
    document.getElementById("notice1").hidden = false;
    let reg = RegExp( this.searchInput );
    console.log("输入内容: ");
    console.log(this.searchInput);
    let dataFound: FriendInfo[] = [];
    for (const soloInfo of this.friendsData) {
      if ( reg.test( soloInfo.name)) {
        dataFound.push( soloInfo );
      }
    }
    console.log("找到的数据：");
    console.log(dataFound);
    // document.getElementById("inner-friends-list").hidden = true;
    this.searchData = dataFound;
    return dataFound;
  }

  addFriend(newFriend: FriendInfo): void {
    this.friendsData.push(newFriend);
    this.instanceInfo = newFriend;
    this.friendsData = this.friendsData.sort( (a, b) => {
      return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
    });
    alert("好友请求已发送！");
  }

//   groupFriends() {
//     for (const soloInfo of this.friendsInfo) {
//       if (this.groups.includes(soloInfo.group)) {
//         this.groups.push(soloInfo.group);
//       }
//     }
//   }
// }

  showSearchInfo(): void {
    document.getElementById("inner-friends-list").hidden = true;
    document.getElementById("search-result").hidden = false;
    // document.getElementById("search-result").innerHTML =
    //   "<div>" +
    //   "<span style='text-align: center; color: red;'>" + "请输入搜索内容" + "</span>" +
    //   "</div>";

  }

  hideSearchInfo(): void {
    console.log(this.searchInput);
    if (this.searchInput === undefined || this.searchInput === "") {
      document.getElementById("inner-friends-list").hidden = false;
      document.getElementById("search-result").hidden = true;

    }
  }

  showFriendInfo(info: FriendInfo): void {
    this.instanceInfo = info;
    document.getElementById("searchButton").hidden = true;

  }

  showNewFriendInfo(info: FriendInfo): void {
    this.instanceInfo = info;
    document.getElementById("searchButton").hidden = false;
  }
}

class FriendInfo {
  accountNumber: string;
  name: string;
  remark: string;
  gender: string;
  birthday: string;
  age: number;
  // constellation: string;
  // yearOfBirth: string;
  imgURL: string;
  constructor(accountNumber: string, name, remark, gender, birthday, age, imgURL) {
    this.accountNumber = accountNumber;
    this.name = name;
    this.remark = remark;
    this.gender = gender;
    this.birthday = birthday;
    this.age = age;
    // this.constellation = constellation;
    // this.yearOfBirth = yearOfBirth;
    this.imgURL = imgURL;
  }
}


function randomString(len: number): string {
  const $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
  const maxPos = $chars.length;
  let pwd = '';
  for (let i = 0; i < len; i++) {
    pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
  }
  console.log(pwd);
  return pwd;
}
function randomAccountNumber(): string {
  const $chars = '0123456789';
  const accountLen = 11;
  let pwd = '';
  for (let i = 0; i < accountLen; i++) {
    pwd += $chars.charAt(Math.floor(Math.random() * accountLen));
  }
  return pwd;
}

function randomData(len: number): FriendInfo[] {
  let data: FriendInfo[] = [];
  for ( let i = 0; i < len; i++) {
    data.push(new FriendInfo(randomAccountNumber(), randomString(10), randomString(6),
      Math.floor(Math.random() * 2) ? '男' : '女', "1949/10/1 ", Math.floor(Math.random()* 80),
      '../../assets/images/' + Math.floor(Math.random() * 5 + 1) + '.jpg'));
  }
  return data;
}





