import {Component, OnInit} from '@angular/core';
import {isEmpty} from "rxjs/operators";
import {User} from '../../../system/user_module/user';
import {UserService} from '../../../system/user_module/user.service';


@Component({
  selector: 'app-friend-info',
  templateUrl: './friend-info.component.html',
  styleUrls: ['./friend-info.component.css']
})
export class FriendInfoComponent implements OnInit {

  private instanceInfo: User;
  private searchInput: string;
  friendsData: User[];
  searchData: User[];

  // private Groups: Group[] = Group.Groups;
  constructor(private user: UserService) {

  }

  ngOnInit() {
    this.friendsData = this.getFriends();
    this.instanceInfo = this.friendsData[0];
  }

  getFriends() {
    let friendsData;
    this.user.getFriends().subscribe(friends => friendsData = friends);
    friendsData = friendsData.sort( (a, b) => {
      return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
    });
    return friendsData;
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


  searchFriend(): User[] {
    if (this.searchInput === undefined || this.searchInput === "") {
      this.searchData = [];
      document.getElementById("notice1").hidden = true;
      return;
    }
    document.getElementById("notice1").hidden = false;

    let reg = RegExp( this.searchInput );

    let dataFound: User[] = [];

    for (const soloInfo of this.friendsData)
      if (reg.test(soloInfo.name))
        dataFound.push(soloInfo);

    this.user.searchFriend(this.searchInput).subscribe(
      data=>{if(data) dataFound.push(data);}
    );

    this.searchData = dataFound;

    return dataFound;
  }

  addFriend(newFriend: User): void {
    this.user.addFriend(newFriend.id).subscribe(
      ()=>alert("好友请求已发送！")
    );
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

  showFriendInfo(info: User): void {
    this.instanceInfo = info;
    document.getElementById("searchButton").hidden = true;

  }

  showNewFriendInfo(info: User): void {
    this.instanceInfo = info;
    document.getElementById("searchButton").hidden = false;
  }


}





