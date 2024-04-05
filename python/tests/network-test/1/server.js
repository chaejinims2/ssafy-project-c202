const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const multer = require('multer');
const fs = require('fs');

// WebSocket 연결
io.on('connection', (socket) => {
  console.log('A client connected');

  // 이미지 데이터 수신
  socket.on('image', (data) => {
    console.log('Received image data');
    // 이미지 데이터를 클라이언트로 전송
    socket.emit('image', data);
  });

  // 연결 종료 시 처리
  socket.on('disconnect', () => {
    console.log('A client disconnected');
  });
});

// 이미지를 저장할 디렉토리 설정
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

// 이미지를 받을 라우트 설정
const upload = multer({ storage: storage });
app.post('/data', upload.single('image'), (req, res) => {
  try {
    console.log('Received image');
    // 이미지 파일을 읽어서 데이터를 클라이언트로 전송
    fs.readFile(req.file.path, (err, data) => {
      if (err) throw err;
      io.emit('image', data);
    });
    res.status(200).send('Image received');
  } catch (error) {
    console.error(error);
    res.status(500).send('An error occurred while processing the image.');
  }
});

// 서버 실행
const PORT = process.env.PORT || 3000;
http.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
