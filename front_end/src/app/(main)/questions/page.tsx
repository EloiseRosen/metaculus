import { Suspense } from "react";

import QuestionTopics from "@/app/(main)/questions/components/question_topics";
import { generateFiltersFromSearchParams } from "@/app/(main)/questions/helpers/filters";
import QuestionFilters from "@/components/question_filters";
import AwaitedQuestionsFeed from "@/components/questions_feed";
import LoadingIndicator from "@/components/ui/loading_indicator";
import ProjectsApi from "@/services/projects";

export default async function Questions({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const filters = generateFiltersFromSearchParams(searchParams);

  const [topics, categories, tags] = await Promise.all([
    ProjectsApi.getTopics(),
    ProjectsApi.getCategories(),
    ProjectsApi.getTags(),
  ]);

  return (
    <main className="mx-auto mt-4 min-h-min w-full max-w-5xl flex-auto px-0 sm:px-2 md:px-3">
      <div className="gap-3 p-0 sm:flex sm:flex-row sm:gap-4">
        <QuestionTopics topics={topics} />
        <div className="min-h-[calc(100vh-300px)] grow overflow-x-hidden p-2 pt-2.5 no-scrollbar sm:p-0 sm:pt-5">
          <QuestionFilters categories={categories} tags={tags} />
          <Suspense
            key={JSON.stringify(searchParams)}
            fallback={
              <LoadingIndicator className="mx-auto h-8 w-24 text-gray-600 dark:text-gray-600-dark" />
            }
          >
            <AwaitedQuestionsFeed filters={filters} />
          </Suspense>
        </div>
      </div>
    </main>
  );
}