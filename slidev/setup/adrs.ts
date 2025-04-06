import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { execSync } from 'child_process';

interface ADRMetadata {
  title: string;
  status: string;
  related: string[];
  decision_makers: string[];
  date: string;
  fileName: string;
  url: string;
}

const adrFolderPath = process.argv[2] || path.join(__dirname, 'ADRs');
const outputFilePath = path.join(__dirname, 'adr-data.json');
const repo = process.argv[3];
const ref = process.argv[4];

const generateAdrData = (): void => {
  const adrFiles = fs.readdirSync(adrFolderPath).filter(file => file.endsWith('.md'));
  const adrData: ADRMetadata[] = adrFiles.map(file => {
    const filePath = path.join(adrFolderPath, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const { data } = matter(content);
    const relativeFilePath = getRelativeFilePath(filePath);
    const metadata: ADRMetadata = {
      title: data.title || 'Untitled',
      status: data.status || 'unknown',
      related: data.related || [],
      decision_makers: data.decision_makers || [],
      date: data.date || 'N/A',
      fileName: file,
      url: `${repo}/blob/${ref}/${relativeFilePath}`
    };

    return metadata;
  });

  fs.writeFileSync(outputFilePath, JSON.stringify(adrData, null, 2));
  console.log('ADR data has been generated at', outputFilePath);
};

const getGitRootDir = (): string => {
  try {
    const rootDir = execSync('git rev-parse --show-toplevel').toString().trim();
    return rootDir;
  } catch (error) {
    console.error('Error getting the Git root directory:', error);
    return process.cwd();
  }
};

const getRelativeFilePath = (filePath: string): string => {
  const gitRootDir = getGitRootDir();
  const relativePath = path.relative(gitRootDir, filePath);
  return relativePath.split(path.sep).join('/');
};

generateAdrData();
