import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FileText, Upload } from 'lucide-react';

export default function FileDropzone({ file, onFileChange }) {
  const onDrop = useCallback(
    (accepted) => {
      if (accepted[0]) onFileChange(accepted[0]);
    },
    [onFileChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={`cursor-pointer rounded-2xl border-2 border-dashed p-10 text-center transition ${
        isDragActive
          ? 'border-brand-500 bg-brand-50 dark:bg-brand-950/30'
          : 'border-slate-300 hover:border-brand-400 dark:border-slate-700'
      }`}
    >
      <input {...getInputProps()} />
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-brand-100 dark:bg-brand-900/50">
        {file ? (
          <FileText className="h-7 w-7 text-brand-600" />
        ) : (
          <Upload className="h-7 w-7 text-brand-600" />
        )}
      </div>
      {file ? (
        <>
          <p className="font-semibold text-slate-800 dark:text-slate-200">{file.name}</p>
          <p className="mt-1 text-sm text-slate-500">Click or drag to replace</p>
        </>
      ) : (
        <>
          <p className="font-semibold text-slate-800 dark:text-slate-200">
            {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume PDF'}
          </p>
          <p className="mt-1 text-sm text-slate-500">or click to browse · Max 10MB</p>
        </>
      )}
    </div>
  );
}
