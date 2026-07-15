import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const skillsRoot = path.join(root, "skills");
const errors = [];
const requiredRootFiles = [
  "README.md",
  "LICENSE",
  "NOTICE",
  "SECURITY.md",
  "CONTRIBUTING.md",
  "CODE_OF_CONDUCT.md",
  "skills.sh.json",
];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await walk(fullPath)));
    else files.push(fullPath);
  }
  return files;
}

function parseFrontmatter(content, file) {
  const match = content.match(/^---\n([\s\S]*?)\n---(?:\n|$)/);
  if (!match) {
    errors.push(`${file}: missing YAML frontmatter`);
    return null;
  }

  const metadata = {};
  for (const rawLine of match[1].split("\n")) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const separator = line.indexOf(":");
    if (separator < 1) {
      errors.push(`${file}: unsupported frontmatter line: ${rawLine}`);
      continue;
    }
    const key = line.slice(0, separator).trim();
    let value = line.slice(separator + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    metadata[key] = value;
  }
  return metadata;
}

function validatePortableContent(content, relativePath) {
  const forbidden = [
    [/\/Users\//, "local macOS path"],
    [/[A-Z]:\\\\Users\\\\/i, "local Windows path"],
    [/mcp__worldos__/i, "client-specific MCP tool prefix"],
    [/\$worldos-[a-z0-9-]+/i, "Codex-specific explicit skill syntax"],
    [/\/worldos:[a-z0-9-]+/i, "Claude-specific plugin skill syntax"],
    [/\[TODO(?::|\])/i, "unresolved TODO placeholder"],
    [/gh[opsu]_[A-Za-z0-9]{20,}/, "possible GitHub token"],
    [/sk-[A-Za-z0-9]{20,}/, "possible API key"],
  ];

  for (const [pattern, label] of forbidden) {
    if (pattern.test(content)) errors.push(`${relativePath}: contains ${label}`);
  }
}

async function validateLinks(content, file) {
  const linkPattern = /\[[^\]]+\]\(([^)]+)\)/g;
  for (const match of content.matchAll(linkPattern)) {
    const target = match[1].split("#", 1)[0];
    if (!target || /^(?:https?:|mailto:)/.test(target)) continue;
    const resolved = path.resolve(path.dirname(file), target);
    try {
      await stat(resolved);
    } catch {
      errors.push(`${path.relative(root, file)}: missing linked file ${target}`);
    }
  }
}

for (const relativePath of requiredRootFiles) {
  try {
    await stat(path.join(root, relativePath));
  } catch {
    errors.push(`Missing required repository file ${relativePath}`);
  }
}

const allFiles = await walk(skillsRoot);
const skillFiles = allFiles.filter((file) => path.basename(file) === "SKILL.md");
if (skillFiles.length === 0) errors.push("No SKILL.md files found under skills/");

const skillNames = new Map();
for (const file of skillFiles) {
  const relativePath = path.relative(root, file);
  const content = await readFile(file, "utf8");
  const metadata = parseFrontmatter(content, relativePath);
  validatePortableContent(content, relativePath);
  await validateLinks(content, file);
  if (!metadata) continue;

  const keys = Object.keys(metadata).sort();
  if (keys.join(",") !== "description,name") {
    errors.push(`${relativePath}: shared skill frontmatter must contain only name and description`);
  }

  const name = metadata.name;
  const description = metadata.description;
  if (!name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name.length > 64) {
    errors.push(`${relativePath}: invalid skill name ${JSON.stringify(name)}`);
  }
  if (!description || description.length > 1024 || /[<>]/.test(description)) {
    errors.push(`${relativePath}: invalid description`);
  }

  const folderName = path.basename(path.dirname(file));
  if (name && folderName !== name) {
    errors.push(`${relativePath}: folder ${folderName} does not match skill name ${name}`);
  }
  if (name && skillNames.has(name)) {
    errors.push(`${relativePath}: duplicate skill name also used by ${skillNames.get(name)}`);
  } else if (name) {
    skillNames.set(name, relativePath);
  }
}

for (const file of allFiles) {
  const relativePath = path.relative(root, file);
  const content = await readFile(file, "utf8");
  validatePortableContent(content, relativePath);
}

for (const relativePath of ["README.md", "SECURITY.md", "CONTRIBUTING.md", "examples/prompts.md"]) {
  const file = path.join(root, relativePath);
  try {
    const content = await readFile(file, "utf8");
    await validateLinks(content, file);
    validatePortableContent(content, relativePath);
  } catch (error) {
    if (error?.code === "ENOENT") errors.push(`Missing required repository file ${relativePath}`);
    else throw error;
  }
}

const pageConfig = JSON.parse(await readFile(path.join(root, "skills.sh.json"), "utf8"));
for (const grouping of pageConfig.groupings ?? []) {
  for (const name of grouping.skills ?? []) {
    if (!skillNames.has(name)) errors.push(`skills.sh.json: unknown skill ${name}`);
  }
}

if (errors.length) {
  console.error(`Validation failed with ${errors.length} error(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Validated ${skillFiles.length} portable WorldOS skill(s).`);
