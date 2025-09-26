
type Props = { kind: "ALERT" | "DANGER" | "SUCCESS" | "WARNING" | "DARK", message: string }


export default function Alert({ kind, message }: Props) {

  switch (kind) {
    case "ALERT":
      return (
        <div className="p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400" role="alert">
          <span className="font-bold text-md">
            {message}
          </span>
        </div>
      )
    case "DANGER":
      return (
        <div className="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
          <span className="font-bold text-md">
            {message}
          </span>
        </div>
      )
    case "SUCCESS":
      return (
        <div className="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert">
          <span className="font-bold text-md">
            {message}
          </span>
        </div>
      )
    case "WARNING":
      return (
        <div className="p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50 dark:bg-gray-800 dark:text-yellow-300" role="alert">
          <span className="font-bold text-md">
            {message}
          </span>
        </div>
      )
    case "DARK":
      return (
        <div className="p-4 text-sm text-gray-800 rounded-lg bg-slate-500 dark:bg-gray-800 dark:text-gray-300" role="alert">
          <span className="font-bold text-md">
            {message}
          </span>
        </div>
      )
  }
}


