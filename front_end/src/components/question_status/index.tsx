import { useLocale, useTranslations } from "next-intl";
import React, { FC, useMemo } from "react";

import QuestionStatusIcon from "@/components/question_status/status_icon";
import {
  Question,
  QuestionStatus as QuestionStatusEnum,
} from "@/types/question";
import { formatRelativeDate } from "@/utils/date_formatters";
import { getQuestionStatus } from "@/utils/forecasts";

type Props = {
  question: Question;
};

// TODO: revisit this component once BE provide all data, required for status definition
const QuestionStatus: FC<Props> = ({ question }) => {
  const t = useTranslations();
  const locale = useLocale();
  const status = getQuestionStatus(question);

  const statusInfo = useMemo(() => {
    if (status === QuestionStatusEnum.Opens) {
      return [
        t("opens"),
        formatRelativeDate(locale, new Date(question.published_at), {
          short: true,
        }),
      ];
    }

    if (status === QuestionStatusEnum.Closes) {
      return [
        t("closes"),
        formatRelativeDate(locale, new Date(question.closed_at), {
          short: true,
        }),
      ];
    }

    if (status === QuestionStatusEnum.Resolves) {
      return [
        t("resolves"),
        formatRelativeDate(locale, new Date(question.resolved_at), {
          short: true,
        }),
      ];
    }

    return [];
  }, [
    locale,
    question.closed_at,
    question.published_at,
    question.resolved_at,
    status,
    t,
  ]);

  return (
    <div className="flex flex-row items-center gap-1.5 truncate text-metac-gray-900 dark:text-metac-gray-900-dark">
      <QuestionStatusIcon
        status={status}
        published_at={question.published_at}
        closed_at={question.closed_at}
      />
      <span className="whitespace-nowrap text-sm">
        {statusInfo.map((part) => (
          <React.Fragment key={`${question.id}-status-${part}`}>
            {part + " "}
          </React.Fragment>
        ))}
      </span>
    </div>
  );
};

export default QuestionStatus;