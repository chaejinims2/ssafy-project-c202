팀코드
    C202

특화트랙
    1.인공지능(영상)

제공구분
    EC2 기본

서버명
    J10C202

서버접속정보
    ssh -i 

비고
    - 주의 : ufw는 반드시 enable 상태로 유지하기
    - [CI/CD] Jenkins 설치 가이드 참고 https://project.ssafy.com > Help > 매뉴얼 게시판

---


메뉴얼 - ufw


제공되는 EC2의 ufw(우분투 방화벽)는 기본적으로 활성화(Enable) 되어 있고, ssh 22번 포트만 접속 가능하게 되어 있습니다. 
포트를 추가할 경우 6번부터 참고하시고,
처음부터 새로 세팅해 보실 경우에는 1번부터 참고하시기 바랍니다.
(ufw: Enable, ssh : 22번 포트)

J10C202

ufw 상태 확인
```shell
$ sudo ufw status
```
사용할 포트 허용하기 (ufw inactive 상태)
```shell
$ sudo ufw allow 22
```
등록한 포트 조회하기 (ufw inactive 상태)
$ sudo ufw show added

ufw 활성화 하기
```shell
$ sudo ufw enable
```
ufw 상태 및 등록된 rule 확인하기
```shell
$ sudo ufw status numbered
```
새로운 터미널을 띄워 ssh 접속해 본다.
(ex : C:\> ssh -i 팀.pem [ubuntu@팀.p.ssafy.io]
```

$ ssh -i 
```
ufw 구동된 상태에서 80 포트 추가하기 (allow 명령을 수행하면 자동으로 ufw에 반영되어 접속이 가능하다. )
```shell
$ sudo ufw allow 80
```
80 포트 정상 등록되었는지 확인하기
```shell
$ sudo ufw status numbered
```
등록한 80 포트 삭제 하기
삭제할 80 포트의 [번호]를 지정하여 삭제하기 (번호 하나씩 지정하여 삭제한다.)
```shell
$ sudo ufw delete 4
$ sudo ufw delete 2
$ sudo ufw status numbered  (제대로 삭제했는지 조회해보기)
```
삭제한 정책은 반드시 enable을 수행해야 적용된다.
```shell
$ sudo ufw enable
```
기타 - ufw 끄기
```shell
$ sudo ufw disable
```
