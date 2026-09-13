import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {visualTutorPlugin} from './server/visualTutor';
export default defineConfig({plugins:[react(),visualTutorPlugin()],server:{host:'127.0.0.1',port:5173,strictPort:true}});
