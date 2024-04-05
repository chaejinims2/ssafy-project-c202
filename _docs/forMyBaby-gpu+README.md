팀코드
    C202

특화트랙
    1.인공지능(영상)

제공구분
    GPU

서버명
    jupyter 계정 : j10c202

서버접속정보 (최초 로그인 시 직접 입력한 패스워드로 자동 저장)
    주피터 URL : http://70.12.130.121 

GPU Device 번호
    Device 1

비고
    - 주의) 배정된 GPU device 번호를 반드시 지정헤서 사용 
    - project.ssafy.com > Help > 매뉴얼 참고 [특화] 교육생 GPU 개발 서버 사용 안내

---

메뉴얼
1. 서버 VPN 설정 - VPN 접속 및 연결

    
        ID :  / PW : 
2. JupyterHub 접속

    
        ID : j10c202 / PW : 
    
    - cf) session time : 24H (주피터 터미널에서 nohup이나 tmux로 background 방식으로 실행해도 세션이 만료된다면 프로세스 종료)
3. 프로그램 실행 시 디바이스 번호 지정하기 (공유 서버 리소스 독점 방지)

    **[GPU Device  번호 지정 : Device 1]**

    ```python
    import os
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"]="1"
    ```

    **[해당 Device 프로세스 실행 확인]**

    ```bash
    // 프로세스 영역 PID 번호 확인
    $ nvidia-smi

    // 해당 PID 번호 user명 확인
    $ ps-ef|grep (PID 번호)
    ```

    **[터미널 접속 및 설정] - 주피터 허브에서만 가능**

    ```bash
    // GPU Device 정보 및 리소스 현황 확인
    // (디바이스 정보 및 메모리 사용률, 실행 프로세스 확인 가능)
    $ nvidia-smi

    // 팀 프로세스 강제 종료 (팀 프로세스 조회 및 강제 종료)
    $ ps-ef|grep 
    $ kill-9 (프로세스 번호)

    // 서버 리소스 사용량 확인 방법 (CPU% 컬럼을 마우스 클릭 -> 사용률 오름차순 정렬)
    $ htop
    ```
