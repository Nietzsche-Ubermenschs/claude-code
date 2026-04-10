import { describe, it, expect } from "bun:test";
import { extractDuplicateIssueNumber } from "./auto-close-duplicates";

describe("extractDuplicateIssueNumber", () => {
  it("should extract issue number from #123 format", () => {
    expect(extractDuplicateIssueNumber("This is a duplicate of #123")).toBe(123);
  });

  it("should extract issue number from GitHub URL format", () => {
    expect(
      extractDuplicateIssueNumber(
        "Duplicate of https://github.com/anthropics/claude-code/issues/456"
      )
    ).toBe(456);
  });

  it("should handle issue numbers at the beginning of the string", () => {
    expect(extractDuplicateIssueNumber("#789 is the original")).toBe(789);
  });

  it("should return null if no issue number is found", () => {
    expect(extractDuplicateIssueNumber("No duplicates here")).toBeNull();
  });

  it("should handle URLs with trailing slashes", () => {
    expect(
      extractDuplicateIssueNumber(
        "https://github.com/anthropics/claude-code/issues/123/"
      )
    ).toBe(123);
  });

  it("should not match non-issue references like hex codes or anchors", () => {
    expect(extractDuplicateIssueNumber("Color is #abc")).toBeNull();
    expect(extractDuplicateIssueNumber("See section #intro")).toBeNull();
  });

  it("should avoid matching part of a word with #", () => {
    expect(extractDuplicateIssueNumber("myissue#123")).toBeNull();
  });

  it("should handle multiple issue numbers by picking the first match", () => {
    expect(extractDuplicateIssueNumber("Duplicates #123 and #456")).toBe(123);
  });

  it("should handle mixed formats", () => {
    expect(
      extractDuplicateIssueNumber(
        "Refer to https://github.com/a/b/issues/1 and #2"
      )
    ).toBe(2); // Current implementation checks # pattern first
  });

  it("should handle punctuation and surrounding characters for # format", () => {
    expect(extractDuplicateIssueNumber("Duplicate of (#123)")).toBe(123);
    expect(extractDuplicateIssueNumber("See [#456]")).toBe(456);
    expect(extractDuplicateIssueNumber("Fixed in **#789**")).toBe(789);
    expect(extractDuplicateIssueNumber("It is #123.")).toBe(123);
  });

  it("should handle trailing characters in URL format", () => {
    expect(
      extractDuplicateIssueNumber(
        "Duplicate of https://github.com/owner/repo/issues/123 and more"
      )
    ).toBe(123);
    expect(
      extractDuplicateIssueNumber(
        "See https://github.com/owner/repo/issues/456."
      )
    ).toBe(456);
    expect(
      extractDuplicateIssueNumber(
        "Link: https://github.com/owner/repo/issues/789)"
      )
    ).toBe(789);
  });
});
