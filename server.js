// const express = require('express');
// const multer = require('multer');
// const ffmpeg = require('fluent-ffmpeg');
// const path = require('path');
// const fs = require('fs');

// const app = express();
// const PORT = 3000;

// // Set storage engine
// const storage = multer.diskStorage({
//   destination: './uploads/',
//   filename: (req, file, cb) => {
//     cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
//   }
// });

// // Initialize upload
// const upload = multer({
//   storage: storage,
//   limits: { fileSize: 100000000 },
//   fileFilter: (req, file, cb) => {
//     checkFileType(file, cb);
//   }
// }).fields([
//   { name: 'characterImage', maxCount: 1 },
//   { name: 'videoTemplate', maxCount: 1 },
//   { name: 'musicFile', maxCount: 1 }
// ]);

// // Check file type
// function checkFileType(file, cb) {
//   const filetypes = /jpeg|jpg|png|gif|mp4|mp3/;
//   const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
//   const mimetype = filetypes.test(file.mimetype);

//   if (mimetype && extname) {
//     return cb(null, true);
//   } else {
//     cb('Error: Images, Videos, and Music Files Only!');
//   }
// }

// // Static folder
// app.use(express.static('./public'));

// // Handle file upload and video processing
// app.post('/upload', (req, res) => {
//   upload(req, res, (err) => {
//     if (err) {
//       res.status(400).json({ message: err });
//     } else {
//       if (req.files == undefined) {
//         res.status(400).json({ message: 'No file selected!' });
//       } else {
//         const characterImagePath = req.files.characterImage[0].path;
//         const videoTemplatePath = req.files.videoTemplate[0].path;
//         const musicFilePath = req.files.musicFile[0].path;
//         const outputFilePath = 'outputs/output-' + Date.now() + '.mp4';

//         ffmpeg()
//           .input(videoTemplatePath)
//           .input(characterImagePath)
//           .input(musicFilePath)
//           .complexFilter([
//             '[0:v][1:v]overlay=x=(W-w)/2:y=(H-h)/2:enable=between(t,0,10)[video]',
//             '[2:a]asplit[main][beats]',
//             '[beats]showwaves=s=1280x720:colors=white:mode=line,format=yuv420p[v]',
//             '[main][v]overlay[out]'
//           ])
//           .outputOptions('-map', '[out]', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', '-movflags', '+faststart')
//           .save(outputFilePath)
//           .on('end', () => {
//             res.download(outputFilePath, (err) => {
//               if (err) console.error(err);
//               fs.unlinkSync(characterImagePath);
//               fs.unlinkSync(videoTemplatePath);
//               fs.unlinkSync(musicFilePath);
//               fs.unlinkSync(outputFilePath);
//             });
//           })
//           .on('error', (err) => {
//             console.error(err);
//             res.status(500).json({ message: 'Error processing video.' });
//           });
//       }
//     }
//   });
// });

// app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
const express = require('express');
const multer = require('multer');
const ffmpeg = require('fluent-ffmpeg');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Set storage engine
const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

// Initialize upload
const upload = multer({
  storage: storage,
  limits: { fileSize: 100000000 },
  fileFilter: (req, file, cb) => {
    checkFileType(file, cb);
  }
}).fields([
  { name: 'characterImage', maxCount: 1 },
  { name: 'videoTemplate', maxCount: 1 },
  { name: 'musicFile', maxCount: 1 }
]);

// Check file type
function checkFileType(file, cb) {
  const filetypes = /jpeg|jpg|png|gif|mp4|mp3/;
  const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = filetypes.test(file.mimetype);

  if (mimetype && extname) {
    return cb(null, true);
  } else {
    cb('Error: Images, Videos, and Music Files Only!');
  }
}

// Static folder
app.use(express.static('./public'));

// Handle file upload and video processing
app.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      res.status(400).json({ message: err });
    } else {
      if (req.files == undefined) {
        res.status(400).json({ message: 'No file selected!' });
      } else {
        const characterImagePath = req.files.characterImage[0].path;
        const videoTemplatePath = req.files.videoTemplate[0].path;
        const musicFilePath = req.files.musicFile[0].path;
        const outputFilePath = 'outputs/output-' + Date.now() + '.mp4';

        ffmpeg()
          .input(videoTemplatePath)
          .input(characterImagePath)
          .input(musicFilePath)
          .complexFilter([
            '[0:v][1:v]overlay=x=(W-w)/2:y=(H-h)/2:enable=between(t,0,10)[video]',
            '[2:a]asplit[main][beats]',
            '[beats]showwaves=s=1280x720:colors=white:mode=line,format=yuv420p[v]',
            '[main][v]overlay[out]'
          ])
          .outputOptions('-map', '[out]', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', '-movflags', '+faststart')
          .save(outputFilePath)
          .on('end', () => {
            res.download(outputFilePath, (err) => {
              if (err) console.error(err);
              fs.unlinkSync(characterImagePath);
              fs.unlinkSync(videoTemplatePath);
              fs.unlinkSync(musicFilePath);
              fs.unlinkSync(outputFilePath);
            });
          })
          .on('error', (err) => {
            console.error(err);
            res.status(500).json({ message: 'Error processing video.' });
          });
      }
    }
  });
});

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
