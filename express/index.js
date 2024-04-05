const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const multer = require('multer');
const fs = require('fs');
//const bodyParser = require('body-parser'); // 설치한 body-parser를 import

app.use(express.json());
app.use(express.urlencoded({extended: true}));


// 방 정보를 저장할 객체
const rooms = {};

let currentStatus = false; // 초기 상태 설정

// WebSocket 연결
io.on('connection', (socket) => {
  console.log('A client connected');

  // 이미지 데이터 수신
  socket.on('image', (data) => {
    console.log('Received image data');
    // 이미지 데이터를 클라이언트로 전송o
    socket.emit('image', data);
  });

  // 클라이언트로부터 아이디 수신
  socket.on('babyId', (babyId) => {
    console.log(`Received babyId: ${babyId}`);
    
    // 해당 아이디와 같은 방이 없으면 방 생성
    if (!rooms[babyId]) {
      rooms[babyId] = [socket.id];
      console.log(`Created room for babyId: ${babyId}`);

      // uploads 폴더 밑에 babyId와 같은 이름의 폴더 생성
      const folderPath = `uploads/${babyId}`;
      fs.mkdir(folderPath, { recursive: true }, (err) => {
        if (err) {
          console.error(`Error creating folder for babyId ${babyId}:`, err);
        } else {
          console.log(`Created folder for babyId: ${babyId}`);
        }
      });
    } else {
      // 이미 해당 아이디와 같은 방이 있으면 해당 방에 소켓 추가
      rooms[babyId].push(socket.id);
      console.log(`Added socket to room for babyId: ${babyId}`);
    }
  });

  // 클라이언트로부터 상태 수신 (실시간 영상 데이터가 필요한지 여부 확인용): true면 필요, false면 불필요
  socket.on('status', (status) => {
    console.log(`Received status: ${status}`);
    if (currentStatus != status){
      currentStatus = status;
    }
  });

  // 연결 종료 시 처리
  socket.on('disconnect', () => {
    console.log('A client disconnected');

    // 소켓이 속한 방 찾아서 소켓 제거
    for (const [roomId, sockets] of Object.entries(rooms)) {
      const index = sockets.indexOf(socket.id);
      if (index !== -1) {
        sockets.splice(index, 1);
        console.log(`Removed socket from room: ${roomId}`);
        // if (sockets.length === 0) {
        //   // 방에 소켓이 없으면 방 삭제
        //   delete rooms[roomId];
        //   console.log(`Deleted room: ${roomId}`);
        // }
        break;
      }
    }
  });
});

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // 클라이언트로부터 전달된 babyId를 확인하여 해당 폴더에 저장
    const babyId = req.body.baby_id;
    const destinationPath = `uploads/${babyId}`;
    // 폴더가 없으면 생성
    fs.mkdir(destinationPath, { recursive: true }, (err) => {
      if (err) {
        console.error(`Error creating folder for babyId ${babyId}:`, err);
      }
    });
    // 저장할 경로를 설정
    cb(null, destinationPath);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

// 영상 데이터 필요 여부 체크
app.post('/check', (req, res) => {
  try {
    const { timestamp } = req.body;
    console.log(`실시간 영상 필요 여부 체크: ${timestamp}`);
    console.log("check함수 실행!*************************")
    res.status(200).send(currentStatus);
  } catch{
    console.error(error);
    res.status(500).send('체크 에러!');
  }
})


// 이미지, 시간, 온습도를 받을 라우트 설정
const upload = multer({ storage: storage });
app.post('/data', upload.single('frame'), (req, res) => {
  try {
    // const babyId = req.params.babyId;
    //console.log('Received image for babyId:', babyId);
    console.log("data함수 실행!*************************")
    const imageFile = req.file;
    const body = req.body; // line 데이터 수신

    // 받은 데이터 확인
    console.log('Received image:', imageFile);
    console.log('Received data:', body);
    console.log('***********************');
    // 시간과 온습도 등의 데이터 추출
    const babyId = body.baby_id;
    const timestamp = body.timestamp;
    const temperature = body.TH[0];
    const humidity = body.TH[1];

    console.log('Received babyId:', babyId);
    console.log('Received timestamp:', timestamp);
    console.log('Received temperature:', temperature);
    console.log('Received humidity:', humidity);
    console.log('***********************');
    // 이미지 파일을 읽어서 데이터를 클라이언트로 전송
    // fs.readFile(imageFile.path, (err, data) => {
    //   if (err) {
    //     console.error('Error reading image file:', err);
    //     res.status(500).send('이미지 파일 읽기 실패!!');
    //     return;
    //   }
      // 이미지와 데이터를 방에 소속된 모든 소켓에게 전송
      io.emit('image', { imageData: imageFile, babyId: babyId, timestamp: timestamp, temp: temperature, humid: humidity });
      // 이미지 데이터를 성공적으로 전송한 후에는 응답을 클라이언트에게 보냅니다.
      res.status(200).send('실시간 영상 전송 성공!');
    // });
  } catch (error) {
    console.error(error);
    res.status(500).send('실시간 영상 전송 실패!');
  }
});


// 이벤트 


app.post('/event', (req, res) => {
  try {
    //const babyId = req.params.baby_id;
    console.log("event함수 실행!*************************")
    //const imageFile = req.file;
    const body = req.body; // line 데이터 수신
    console.log('받은 데이터', req.body);
    //console.log('받은 파일', req.file);
    console.log('***********************');
    const { info, baby_id, timestamp, url_s3 } = req.body;

    //받은 데이터 로깅
    //console.log(`Received sleep event for babyId: ${baby_id}`);
    //console.log(`babyId: ${baby_id}, Timestamp: ${timestamp}, Event type: ${event_type}, detail: ${detail}, url s3: ${url_s3}`);

    if (info[0] == '0'){ // 이벤트 - 위치정보 
      const detail = '1';
      io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
    } else {
        if (info[1] == '0'){ // 수면
            if (info[2] == '0'){ // 잠에서 깸
                const detail = '0';
                io.emit('sleepEvent', { timestamp, detail, baby_id});
            } else { // 잠듦
                const detail = '1';
                io.emit('sleepEvent', { timestamp, detail, baby_id});
            }
        } else if (info[1] == '1'){ // 위험 
            if (info[2] == '0'){ // 위험 - 뒤집기
                const detail = '0';
                io.emit('dangerEvent', {timestamp, detail, baby_id });
            } else if (info[2] == '1'){ // 위험 - 입에 뭐 넣기
                const detail = '1';
                io.emit('dangerEvent', {timestamp, detail, baby_id });
            } else { // 위험 - 추락
                const detail = '2';
                io.emit('dangerEvent', {timestamp, detail, baby_id });
            }
        } else { // 이벤트
            if (info[2] == '0'){ // 스톱모션용
                const detail = '0';
                io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
            } else if (info[2] == '1'){ // 만세
                const detail = '2';
                io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
            } else if (info[2] == '2'){ // 다리꼬기
                const detail = '3';
                io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
            } else {
                const detail = '4';
                io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
            } 
        }
        
      }
      res.status(200).send('이벤트 행동 데이터 전송 완료!');
  //   if (event_type == '2'){ // 수면 관련
  //     if (detail == '0'){ // 잠에서 깸
  //       io.emit('sleepEvent', { timestamp, detail, baby_id});
  //     } else if (detail == '1') { // 잠 듦
  //       io.emit('sleepEvent', { timestamp, detail, baby_id});
  //     }
  //     res.status(200).send('수면 분석 데이터 전송 완료!');
  //   } else if (event_type == '1'){ // 위험 관련
  //     if (detail == '0'){ // 위험행동 - 뒤집기(이전)
  //       io.emit('dangerEvent', {timestamp, detail, baby_id });
  //     }
  //     res.status(200).send('위험 행동 데이터 전송 완료!');
  //   } else { // 스톱모션(0), 만세(1), 다리꼬기(2) 
  //     if (detail == '0'){ // 스톱모션
  //       io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
  //     } else if (detail == '1'){ // 만세
  //       io.emit('commonEvent', { timestamp, detail, baby_id, url_s3 });
  //     } else if (detail == '2'){ // 다리꼬기
  //       io.emit('commonEvenet', { timestamp, detail, baby_id, url_s3 });
  //     }
  //     res.status(200).send('이벤트 행동 데이터 전송 완료!');
  //   }       
  } catch (error) {
    console.error(error);
    res.status(500).send('데이터 전송 실패!');
  } 
});

// 서버 실행
const PORT = process.env.PORT || 8083;
http.listen(PORT, async () => {
  console.log(`Server is running on port ${PORT}`);
});


// 이벤트 (일반 - 스탬프용)
// timestamp; event_type; device_model; device_ID; baby_id
// '/event/:babyId'
// app.post('/event', (req, res) => {
//   try {
//     // const babyId = req.params.babyId;
//     console.log(req.body);
//     const data = req.body;
//     const timestamp = data.timestamp;
//     const event_type = data.event_type;
//     const device_model = data.device_model;
//     const device_ID = data.device_ID;


//     // 받은 데이터 로깅
//     //console.log(`Received sleep event for babyId: ${babyId}`);
//     console.log(`Timestamp: ${timestamp}, Event type: ${event_type}, Device model: ${device_model}, Device ID: ${device_ID}`);

//     // 해당 방에 속한 클라이언트들에게 데이터 전송
//     io.emit('commonEvent', { timestamp, event_type, device_model, device_ID });

//     res.status(200).send('일반 스탬프용 데이터 전송 완료!');
//   } catch (error) {
//     console.error(error);
//     res.status(500).send('일반 스탬프용 데이터 전송 실패!');
//   }
// });


// 이벤트 (위험 - 알림용)
// timestamp; event_type; device_model; device_ID; baby_id
// '/danger/:babyId'
// app.post('/danger', (req, res) => {
//   try {
//     console.log(req.body.data)
//     if (!req.body) {
//       throw new Error('Request body is undefined or empty');
//     }

//     const { timestamp, event_type, device_model, device_ID } = req.body;

//     if (!timestamp || !event_type || !device_model || !device_ID) {
//       throw new Error('One or more required fields are missing in the request body');
//     }

//     // 받은 데이터 로깅
//     console.log('Received data:');
//     console.log(`Timestamp: ${timestamp}, Event type: ${event_type}, Device model: ${device_model}, Device ID: ${device_ID}`);

//     // 해당 방에 속한 클라이언트들에게 데이터 전송
//     io.emit('dangerEvent', { timestamp, event_type, device_model, device_ID });

//     res.status(200).send('위험 알림용 데이터 전송 완료!');
//   } catch (error) {
//     console.error(error);
//     res.status(500).send('위험 알림용 데이터 전송 실패!');
//   }
// });
